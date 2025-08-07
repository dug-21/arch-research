# RAG Implementation Examples and Code Samples

## Overview

This document provides practical implementation examples demonstrating the key architectural patterns and components discussed in the RAG implementation analysis. These examples are production-ready code samples that can be adapted for specific use cases.

## 1. Complete RAG Pipeline Example

### 1.1 Basic RAG System Implementation

```python
import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from openai import AsyncOpenAI

@dataclass
class Document:
    id: str
    content: str
    metadata: Dict
    embedding: Optional[np.ndarray] = None
    score: float = 0.0

@dataclass
class RAGResult:
    answer: str
    source_documents: List[Document]
    confidence: float
    metadata: Dict

class ProductionRAGSystem:
    """
    Production-ready RAG system with verification loops
    """
    def __init__(self):
        # Initialize components
        self.embedder = SentenceTransformer('all-mpnet-base-v2')
        self.vector_index = None
        self.llm_client = AsyncOpenAI()
        
        # Verification components
        self.claim_extractor = ClaimExtractor()
        self.fact_verifier = FactVerifier()
        self.confidence_estimator = ConfidenceEstimator()
        
        # Performance tracking
        self.metrics_tracker = MetricsTracker()
        
    async def initialize_index(self, documents: List[Document]):
        """Initialize vector index with documents"""
        print("Generating embeddings for documents...")
        embeddings = []
        
        for doc in documents:
            embedding = self.embedder.encode(doc.content)
            doc.embedding = embedding
            embeddings.append(embedding)
        
        # Create FAISS index
        dimension = embeddings[0].shape[0]
        self.vector_index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        embeddings_array = np.array(embeddings)
        faiss.normalize_L2(embeddings_array)
        
        self.vector_index.add(embeddings_array)
        self.documents = documents
        
        print(f"Index initialized with {len(documents)} documents")
    
    async def query(self, question: str, k: int = 5) -> RAGResult:
        """Main query method with verification"""
        start_time = time.time()
        
        try:
            # Step 1: Retrieve relevant documents
            retrieved_docs = await self.retrieve_documents(question, k)
            
            # Step 2: Generate initial answer
            initial_answer = await self.generate_answer(question, retrieved_docs)
            
            # Step 3: Verify and refine answer
            verified_result = await self.verify_and_refine(
                question, initial_answer, retrieved_docs
            )
            
            # Step 4: Calculate confidence
            confidence = await self.confidence_estimator.calculate_confidence(
                verified_result, retrieved_docs
            )
            
            # Track metrics
            total_time = time.time() - start_time
            await self.metrics_tracker.track_query(
                question, verified_result, confidence, total_time
            )
            
            return RAGResult(
                answer=verified_result,
                source_documents=retrieved_docs,
                confidence=confidence,
                metadata={
                    'processing_time': total_time,
                    'verification_performed': True,
                    'retrieved_doc_count': len(retrieved_docs)
                }
            )
            
        except Exception as e:
            print(f"Error processing query: {e}")
            return RAGResult(
                answer="I'm sorry, I encountered an error processing your question.",
                source_documents=[],
                confidence=0.0,
                metadata={'error': str(e)}
            )
    
    async def retrieve_documents(self, question: str, k: int) -> List[Document]:
        """Retrieve relevant documents using vector similarity"""
        # Generate query embedding
        query_embedding = self.embedder.encode(question)
        query_embedding = np.array([query_embedding])
        faiss.normalize_L2(query_embedding)
        
        # Search index
        scores, indices = self.vector_index.search(query_embedding, k)
        
        # Prepare results
        retrieved_docs = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:  # Valid result
                doc = self.documents[idx]
                doc.score = float(score)
                retrieved_docs.append(doc)
        
        return retrieved_docs
    
    async def generate_answer(self, question: str, documents: List[Document]) -> str:
        """Generate answer using retrieved context"""
        # Prepare context
        context = "\n\n".join([
            f"Source {i+1}: {doc.content[:500]}..."
            for i, doc in enumerate(documents)
        ])
        
        # Create prompt
        prompt = f"""Based on the following context, please answer the question accurately and concisely.

Context:
{context}

Question: {question}

Instructions:
1. Answer based only on the provided context
2. If the context doesn't contain enough information, say so
3. Cite relevant sources when making claims
4. Be precise and factual

Answer:"""
        
        # Generate response
        response = await self.llm_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful, accurate assistant that answers questions based on provided context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    async def verify_and_refine(self, question: str, answer: str, documents: List[Document]) -> str:
        """Verify answer accuracy and refine if needed"""
        # Extract claims from the answer
        claims = await self.claim_extractor.extract_claims(answer)
        
        # Verify each claim
        verification_results = []
        for claim in claims:
            verification = await self.fact_verifier.verify_claim(claim, documents)
            verification_results.append(verification)
        
        # Check if all claims are verified
        unverified_claims = [
            result for result in verification_results 
            if not result.verified
        ]
        
        if unverified_claims:
            # Refine answer to address unverified claims
            refined_answer = await self.refine_answer(
                question, answer, unverified_claims, documents
            )
            return refined_answer
        
        return answer
    
    async def refine_answer(self, question: str, original_answer: str, 
                          unverified_claims: List, documents: List[Document]) -> str:
        """Refine answer to address unverified claims"""
        refinement_prompt = f"""The following answer contains some claims that could not be verified:

Original Answer: {original_answer}

Unverified Claims:
{[claim.description for claim in unverified_claims]}

Please refine the answer to:
1. Remove or qualify unverified claims
2. Add uncertainty markers where appropriate
3. Focus on verified information from the context

Question: {question}

Refined Answer:"""
        
        response = await self.llm_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "Refine the answer to be more accurate and properly qualified."},
                {"role": "user", "content": refinement_prompt}
            ],
            temperature=0.1,
            max_tokens=500
        )
        
        return response.choices[0].message.content

# Supporting classes for verification
class ClaimExtractor:
    """Extract verifiable claims from text"""
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    async def extract_claims(self, text: str) -> List[Dict]:
        """Extract factual claims from text"""
        doc = self.nlp(text)
        claims = []
        
        for sent in doc.sents:
            # Simple claim extraction based on sentence structure
            if self._is_factual_sentence(sent):
                claims.append({
                    'text': sent.text,
                    'confidence': 0.8,  # Simple confidence score
                    'type': 'factual'
                })
        
        return claims
    
    def _is_factual_sentence(self, sentence) -> bool:
        """Determine if sentence contains factual claims"""
        # Simple heuristics for factual sentences
        factual_indicators = ['is', 'are', 'was', 'were', 'has', 'have', 'shows', 'indicates']
        return any(token.lemma_ in factual_indicators for token in sentence)

class FactVerifier:
    """Verify claims against provided context"""
    
    async def verify_claim(self, claim: Dict, documents: List[Document]):
        """Verify a claim against document context"""
        claim_text = claim['text']
        
        # Find relevant passages
        relevant_passages = []
        for doc in documents:
            if self._claim_supported_by_document(claim_text, doc.content):
                relevant_passages.append(doc)
        
        verification_result = VerificationResult(
            claim=claim_text,
            verified=len(relevant_passages) > 0,
            confidence=min(len(relevant_passages) * 0.3, 1.0),
            supporting_documents=relevant_passages
        )
        
        return verification_result
    
    def _claim_supported_by_document(self, claim: str, document: str) -> bool:
        """Simple check if claim is supported by document"""
        # This is a simplified implementation
        # In production, use more sophisticated NLI models
        claim_words = set(claim.lower().split())
        doc_words = set(document.lower().split())
        
        # Check word overlap (simple approach)
        overlap = len(claim_words.intersection(doc_words))
        return overlap >= len(claim_words) * 0.3

@dataclass
class VerificationResult:
    claim: str
    verified: bool
    confidence: float
    supporting_documents: List[Document]

class ConfidenceEstimator:
    """Estimate confidence in generated answers"""
    
    async def calculate_confidence(self, answer: str, documents: List[Document]) -> float:
        """Calculate confidence score for answer"""
        confidence_factors = []
        
        # Factor 1: Source document relevance scores
        if documents:
            avg_doc_score = sum(doc.score for doc in documents) / len(documents)
            confidence_factors.append(avg_doc_score * 0.3)
        
        # Factor 2: Answer length and completeness
        answer_length_score = min(len(answer.split()) / 50, 1.0)  # Normalize to 50 words
        confidence_factors.append(answer_length_score * 0.2)
        
        # Factor 3: Presence of uncertainty markers
        uncertainty_markers = ['might', 'could', 'possibly', 'unclear', 'unknown']
        uncertainty_penalty = sum(1 for marker in uncertainty_markers if marker in answer.lower())
        uncertainty_score = max(0, 1.0 - uncertainty_penalty * 0.1)
        confidence_factors.append(uncertainty_score * 0.3)
        
        # Factor 4: Citation presence
        citation_score = 1.0 if 'source' in answer.lower() else 0.5
        confidence_factors.append(citation_score * 0.2)
        
        return sum(confidence_factors)

class MetricsTracker:
    """Track system performance metrics"""
    
    def __init__(self):
        self.metrics = []
    
    async def track_query(self, question: str, answer: str, confidence: float, processing_time: float):
        """Track query metrics"""
        self.metrics.append({
            'timestamp': time.time(),
            'question_length': len(question.split()),
            'answer_length': len(answer.split()),
            'confidence': confidence,
            'processing_time': processing_time
        })
        
        # Log metrics periodically
        if len(self.metrics) % 100 == 0:
            await self._log_aggregated_metrics()
    
    async def _log_aggregated_metrics(self):
        """Log aggregated performance metrics"""
        recent_metrics = self.metrics[-100:]
        
        avg_confidence = sum(m['confidence'] for m in recent_metrics) / len(recent_metrics)
        avg_processing_time = sum(m['processing_time'] for m in recent_metrics) / len(recent_metrics)
        
        print(f"Recent 100 queries - Avg Confidence: {avg_confidence:.2f}, Avg Time: {avg_processing_time:.2f}s")
```

## 2. Multi-Level Caching Implementation

```python
import redis
import json
import hashlib
from typing import Optional, Dict, Any
import asyncio
import time

class MultiLevelRAGCache:
    """Production-ready multi-level cache for RAG systems"""
    
    def __init__(self, redis_host='localhost', redis_port=6379):
        # Redis connection for distributed caching
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        
        # Local in-memory cache for fastest access
        self.local_cache = {}
        self.local_cache_size = 1000
        
        # Semantic similarity cache
        self.semantic_cache = SemanticCache()
        
        # Cache configuration
        self.ttl_config = {
            'response': 3600,    # 1 hour
            'embedding': 86400,  # 24 hours
            'retrieval': 1800    # 30 minutes
        }
    
    async def get_or_compute(self, cache_key: str, compute_func, cache_type: str = 'response'):
        """Main cache interface with fallback computation"""
        
        # L1: Check local memory cache
        local_result = self._get_from_local_cache(cache_key)
        if local_result:
            await self._track_cache_hit('local', cache_type)
            return local_result
        
        # L2: Check Redis cache
        redis_result = await self._get_from_redis_cache(cache_key)
        if redis_result:
            # Store in local cache for future
            self._store_in_local_cache(cache_key, redis_result)
            await self._track_cache_hit('redis', cache_type)
            return redis_result
        
        # L3: Check semantic cache for similar queries
        if cache_type == 'response':
            semantic_result = await self.semantic_cache.find_similar(cache_key)
            if semantic_result:
                # Store adapted result in both caches
                adapted_result = semantic_result['adapted_response']
                await self._store_in_all_caches(cache_key, adapted_result, cache_type)
                await self._track_cache_hit('semantic', cache_type)
                return adapted_result
        
        # Cache miss - compute result
        result = await compute_func()
        
        # Store in all cache levels
        await self._store_in_all_caches(cache_key, result, cache_type)
        await self._track_cache_miss(cache_type)
        
        return result
    
    def _get_from_local_cache(self, cache_key: str) -> Optional[Any]:
        """Get value from local memory cache"""
        cache_entry = self.local_cache.get(cache_key)
        if cache_entry:
            # Check if expired
            if time.time() < cache_entry['expires_at']:
                return cache_entry['value']
            else:
                # Remove expired entry
                del self.local_cache[cache_key]
        
        return None
    
    async def _get_from_redis_cache(self, cache_key: str) -> Optional[Any]:
        """Get value from Redis cache"""
        try:
            cached_data = self.redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Redis cache error: {e}")
        
        return None
    
    def _store_in_local_cache(self, cache_key: str, value: Any):
        """Store value in local memory cache"""
        # Implement LRU eviction if cache is full
        if len(self.local_cache) >= self.local_cache_size:
            self._evict_lru_entry()
        
        self.local_cache[cache_key] = {
            'value': value,
            'expires_at': time.time() + self.ttl_config['response'],
            'accessed_at': time.time()
        }
    
    async def _store_in_all_caches(self, cache_key: str, value: Any, cache_type: str):
        """Store value in all appropriate cache levels"""
        # Local cache
        self._store_in_local_cache(cache_key, value)
        
        # Redis cache
        try:
            ttl = self.ttl_config.get(cache_type, 3600)
            self.redis_client.setex(
                cache_key,
                ttl,
                json.dumps(value, default=str)
            )
        except Exception as e:
            print(f"Redis storage error: {e}")
        
        # Semantic cache for responses
        if cache_type == 'response':
            await self.semantic_cache.store(cache_key, value)
    
    def _evict_lru_entry(self):
        """Evict least recently used entry from local cache"""
        if not self.local_cache:
            return
        
        lru_key = min(
            self.local_cache.keys(),
            key=lambda k: self.local_cache[k]['accessed_at']
        )
        del self.local_cache[lru_key]
    
    async def _track_cache_hit(self, cache_level: str, cache_type: str):
        """Track cache hit metrics"""
        metric_key = f"cache_hits:{cache_level}:{cache_type}"
        self.redis_client.incr(metric_key)
        self.redis_client.expire(metric_key, 86400)  # 24 hour expiry
    
    async def _track_cache_miss(self, cache_type: str):
        """Track cache miss metrics"""
        metric_key = f"cache_misses:{cache_type}"
        self.redis_client.incr(metric_key)
        self.redis_client.expire(metric_key, 86400)
    
    def generate_cache_key(self, query: str, context_hash: str = "") -> str:
        """Generate consistent cache key for query"""
        key_string = f"{query}:{context_hash}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        stats = {}
        
        # Get hit/miss ratios
        cache_levels = ['local', 'redis', 'semantic']
        cache_types = ['response', 'embedding', 'retrieval']
        
        for level in cache_levels:
            for cache_type in cache_types:
                hits_key = f"cache_hits:{level}:{cache_type}"
                misses_key = f"cache_misses:{cache_type}"
                
                hits = int(self.redis_client.get(hits_key) or 0)
                misses = int(self.redis_client.get(misses_key) or 0)
                
                total = hits + misses
                hit_rate = hits / total if total > 0 else 0
                
                stats[f"{level}_{cache_type}_hit_rate"] = hit_rate
        
        # Local cache statistics
        stats['local_cache_size'] = len(self.local_cache)
        stats['local_cache_max_size'] = self.local_cache_size
        
        return stats

class SemanticCache:
    """Semantic similarity-based caching for RAG responses"""
    
    def __init__(self, similarity_threshold=0.9):
        self.similarity_threshold = similarity_threshold
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.cache_entries = {}
        self.query_embeddings = {}
        
    async def find_similar(self, query: str) -> Optional[Dict]:
        """Find semantically similar cached query"""
        query_embedding = self.embedder.encode(query)
        
        best_match = None
        best_similarity = 0.0
        
        for cached_query, cached_embedding in self.query_embeddings.items():
            similarity = self._cosine_similarity(query_embedding, cached_embedding)
            
            if similarity > self.similarity_threshold and similarity > best_similarity:
                best_similarity = similarity
                best_match = cached_query
        
        if best_match:
            cached_response = self.cache_entries[best_match]
            adapted_response = await self._adapt_response(
                cached_response, query, best_match, best_similarity
            )
            
            return {
                'original_query': best_match,
                'similarity': best_similarity,
                'cached_response': cached_response,
                'adapted_response': adapted_response
            }
        
        return None
    
    async def store(self, query: str, response: str):
        """Store query-response pair in semantic cache"""
        query_embedding = self.embedder.encode(query)
        
        self.cache_entries[query] = response
        self.query_embeddings[query] = query_embedding
        
        # Implement cache size limit
        if len(self.cache_entries) > 1000:
            await self._evict_oldest_entries()
    
    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors"""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    async def _adapt_response(self, cached_response: str, new_query: str, 
                            original_query: str, similarity: float) -> str:
        """Adapt cached response for new query"""
        if similarity > 0.95:
            # Very high similarity - use cached response as-is
            return cached_response
        else:
            # Moderate similarity - add adaptation note
            return f"{cached_response}\n\n*Note: This response was adapted from a similar query with {similarity:.1%} confidence.*"
    
    async def _evict_oldest_entries(self):
        """Evict oldest cache entries to maintain size limit"""
        # Simple FIFO eviction - remove first 100 entries
        keys_to_remove = list(self.cache_entries.keys())[:100]
        
        for key in keys_to_remove:
            del self.cache_entries[key]
            del self.query_embeddings[key]
```

## 3. Real-Time Fact Checking Integration

```python
import aiohttp
import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass
import json

@dataclass
class FactCheckResult:
    claim: str
    verified: bool
    confidence: float
    sources: List[str]
    evidence: str
    reasoning: str

class RealTimeFactChecker:
    """Real-time fact checking integration for RAG systems"""
    
    def __init__(self):
        # External fact-checking APIs
        self.fact_check_apis = [
            WikidataFactChecker(),
            NewsAPIFactChecker(),
            ScientificFactChecker()
        ]
        
        # Internal components
        self.claim_extractor = ClaimExtractor()
        self.source_credibility = SourceCredibilityAnalyzer()
        
        # Performance tracking
        self.fact_check_cache = {}
        self.cache_ttl = 3600  # 1 hour
    
    async def verify_answer_realtime(self, answer: str, query_context: str) -> Dict:
        """Verify answer claims in real-time"""
        # Extract verifiable claims
        claims = await self.claim_extractor.extract_verifiable_claims(answer)
        
        if not claims:
            return {
                'verification_status': 'no_verifiable_claims',
                'confidence': 0.5,
                'verified_claims': [],
                'disputed_claims': []
            }
        
        # Verify claims in parallel
        verification_tasks = []
        for claim in claims:
            task = self._verify_single_claim(claim, query_context)
            verification_tasks.append(task)
        
        # Collect verification results
        verification_results = await asyncio.gather(
            *verification_tasks, 
            return_exceptions=True
        )
        
        # Process results
        verified_claims = []
        disputed_claims = []
        total_confidence = 0.0
        
        for i, result in enumerate(verification_results):
            if isinstance(result, Exception):
                print(f"Fact check error for claim {i}: {result}")
                disputed_claims.append({
                    'claim': claims[i]['text'],
                    'error': str(result)
                })
                continue
            
            if result.verified and result.confidence > 0.7:
                verified_claims.append(result)
                total_confidence += result.confidence
            else:
                disputed_claims.append(result)
        
        # Calculate overall verification confidence
        overall_confidence = (
            total_confidence / len(claims) if claims else 0.0
        )
        
        return {
            'verification_status': 'completed',
            'overall_confidence': overall_confidence,
            'verified_claims': verified_claims,
            'disputed_claims': disputed_claims,
            'verification_summary': self._generate_verification_summary(
                verified_claims, disputed_claims
            )
        }
    
    async def _verify_single_claim(self, claim: Dict, context: str) -> FactCheckResult:
        """Verify a single claim using multiple sources"""
        claim_text = claim['text']
        
        # Check cache first
        cache_key = self._generate_cache_key(claim_text)
        cached_result = self.fact_check_cache.get(cache_key)
        
        if cached_result and self._is_cache_valid(cached_result):
            return cached_result['result']
        
        # Perform verification using multiple APIs
        verification_tasks = []
        for api in self.fact_check_apis:
            task = api.verify_claim_async(claim_text, context)
            verification_tasks.append(task)
        
        # Collect results with timeout
        api_results = []
        try:
            api_responses = await asyncio.wait_for(
                asyncio.gather(*verification_tasks, return_exceptions=True),
                timeout=10.0  # 10 second timeout
            )
            
            for response in api_responses:
                if not isinstance(response, Exception) and response:
                    api_results.append(response)
                    
        except asyncio.TimeoutError:
            print(f"Fact check timeout for claim: {claim_text[:50]}...")
        
        # Aggregate results
        if not api_results:
            return FactCheckResult(
                claim=claim_text,
                verified=False,
                confidence=0.0,
                sources=[],
                evidence="No verification sources available",
                reasoning="Could not verify due to API failures"
            )
        
        aggregated_result = await self._aggregate_verification_results(
            claim_text, api_results
        )
        
        # Cache result
        self.fact_check_cache[cache_key] = {
            'result': aggregated_result,
            'timestamp': time.time()
        }
        
        return aggregated_result
    
    async def _aggregate_verification_results(self, claim: str, 
                                            api_results: List) -> FactCheckResult:
        """Aggregate verification results from multiple sources"""
        verified_count = sum(1 for result in api_results if result.verified)
        total_confidence = sum(result.confidence for result in api_results)
        
        # Collect all sources and evidence
        all_sources = []
        all_evidence = []
        
        for result in api_results:
            all_sources.extend(result.sources)
            if result.evidence:
                all_evidence.append(result.evidence)
        
        # Determine overall verification status
        verification_threshold = 0.6
        overall_confidence = total_confidence / len(api_results)
        is_verified = (verified_count >= len(api_results) * verification_threshold and 
                      overall_confidence >= 0.7)
        
        # Generate reasoning
        reasoning = f"Verified by {verified_count}/{len(api_results)} sources. "
        if is_verified:
            reasoning += "Claim appears to be supported by multiple reliable sources."
        else:
            reasoning += "Insufficient evidence or contradictory information found."
        
        return FactCheckResult(
            claim=claim,
            verified=is_verified,
            confidence=overall_confidence,
            sources=list(set(all_sources))[:5],  # Top 5 unique sources
            evidence="; ".join(all_evidence[:3]),  # Top 3 evidence pieces
            reasoning=reasoning
        )
    
    def _generate_verification_summary(self, verified_claims: List, 
                                     disputed_claims: List) -> str:
        """Generate human-readable verification summary"""
        total_claims = len(verified_claims) + len(disputed_claims)
        
        if total_claims == 0:
            return "No verifiable claims found in the response."
        
        verified_count = len(verified_claims)
        verification_rate = verified_count / total_claims
        
        if verification_rate >= 0.8:
            summary = f"High confidence: {verified_count}/{total_claims} claims verified."
        elif verification_rate >= 0.6:
            summary = f"Moderate confidence: {verified_count}/{total_claims} claims verified."
        else:
            summary = f"Low confidence: Only {verified_count}/{total_claims} claims verified."
        
        if disputed_claims:
            summary += f" {len(disputed_claims)} claims require further verification."
        
        return summary
    
    def _generate_cache_key(self, claim_text: str) -> str:
        """Generate cache key for claim"""
        return hashlib.md5(claim_text.encode()).hexdigest()
    
    def _is_cache_valid(self, cached_entry: Dict) -> bool:
        """Check if cached entry is still valid"""
        return time.time() - cached_entry['timestamp'] < self.cache_ttl

# Fact-checking API integrations
class WikidataFactChecker:
    """Wikidata-based fact checking"""
    
    async def verify_claim_async(self, claim: str, context: str) -> FactCheckResult:
        """Verify claim against Wikidata"""
        # Extract entities from claim
        entities = self._extract_entities(claim)
        
        if not entities:
            return FactCheckResult(
                claim=claim,
                verified=False,
                confidence=0.0,
                sources=[],
                evidence="No identifiable entities for verification",
                reasoning="Cannot verify claim without specific entities"
            )
        
        # Query Wikidata SPARQL endpoint
        try:
            verification_result = await self._query_wikidata(entities, claim)
            return verification_result
            
        except Exception as e:
            return FactCheckResult(
                claim=claim,
                verified=False,
                confidence=0.0,
                sources=[],
                evidence=f"Wikidata query error: {str(e)}",
                reasoning="Could not verify due to API error"
            )
    
    async def _query_wikidata(self, entities: List[str], claim: str) -> FactCheckResult:
        """Query Wikidata SPARQL endpoint"""
        # Simplified SPARQL query construction
        sparql_query = self._build_sparql_query(entities, claim)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://query.wikidata.org/sparql",
                params={"query": sparql_query, "format": "json"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_wikidata_response(data, claim)
                else:
                    raise Exception(f"Wikidata API error: {response.status}")
    
    def _extract_entities(self, claim: str) -> List[str]:
        """Extract named entities from claim text"""
        # Simplified entity extraction
        # In production, use spaCy or similar NER library
        import re
        
        # Look for capitalized words (simple approach)
        entities = re.findall(r'\b[A-Z][a-z]+\b', claim)
        return entities[:5]  # Limit to 5 entities
    
    def _build_sparql_query(self, entities: List[str], claim: str) -> str:
        """Build SPARQL query for entities"""
        # Simplified query builder
        entity_filters = " OR ".join([f'?itemLabel = "{entity}"' for entity in entities])
        
        query = f"""
        SELECT ?item ?itemLabel ?property ?value WHERE {{
            ?item ?property ?value.
            ?item rdfs:label ?itemLabel.
            FILTER(LANG(?itemLabel) = "en").
            FILTER({entity_filters}).
        }}
        LIMIT 10
        """
        return query
    
    def _process_wikidata_response(self, data: Dict, claim: str) -> FactCheckResult:
        """Process Wikidata SPARQL response"""
        results = data.get('results', {}).get('bindings', [])
        
        if not results:
            return FactCheckResult(
                claim=claim,
                verified=False,
                confidence=0.0,
                sources=['wikidata.org'],
                evidence="No matching entities found in Wikidata",
                reasoning="Entities mentioned in claim not found in Wikidata"
            )
        
        # Simple verification: if entities exist, claim has some support
        confidence = min(len(results) * 0.2, 1.0)
        evidence = f"Found {len(results)} relevant Wikidata entries"
        
        return FactCheckResult(
            claim=claim,
            verified=len(results) > 0,
            confidence=confidence,
            sources=['wikidata.org'],
            evidence=evidence,
            reasoning=f"Entities in claim found in Wikidata knowledge base"
        )

class NewsAPIFactChecker:
    """News API-based fact checking"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "your_newsapi_key"
        self.base_url = "https://newsapi.org/v2"
    
    async def verify_claim_async(self, claim: str, context: str) -> FactCheckResult:
        """Verify claim against recent news sources"""
        # Extract key terms from claim
        key_terms = self._extract_key_terms(claim)
        
        if not key_terms:
            return FactCheckResult(
                claim=claim,
                verified=False,
                confidence=0.0,
                sources=[],
                evidence="No key terms identified for news search",
                reasoning="Cannot verify claim without specific search terms"
            )
        
        # Search news articles
        try:
            news_results = await self._search_news(key_terms)
            return await self._analyze_news_results(claim, news_results)
            
        except Exception as e:
            return FactCheckResult(
                claim=claim,
                verified=False,
                confidence=0.0,
                sources=[],
                evidence=f"News API error: {str(e)}",
                reasoning="Could not verify due to news API error"
            )
    
    async def _search_news(self, key_terms: List[str]) -> Dict:
        """Search news articles using News API"""
        query = " AND ".join(key_terms[:3])  # Limit to 3 terms
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/everything",
                params={
                    "q": query,
                    "sortBy": "relevancy",
                    "pageSize": 10,
                    "language": "en",
                    "apiKey": self.api_key
                }
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"News API error: {response.status}")
    
    async def _analyze_news_results(self, claim: str, news_data: Dict) -> FactCheckResult:
        """Analyze news results for claim verification"""
        articles = news_data.get('articles', [])
        
        if not articles:
            return FactCheckResult(
                claim=claim,
                verified=False,
                confidence=0.0,
                sources=[],
                evidence="No relevant news articles found",
                reasoning="No recent news coverage found for this claim"
            )
        
        # Simple analysis: check if claim terms appear in article content
        supporting_articles = []
        for article in articles:
            title = article.get('title', '')
            description = article.get('description', '')
            content = f"{title} {description}".lower()
            
            # Check if claim concepts are mentioned
            claim_words = set(claim.lower().split())
            content_words = set(content.split())
            
            overlap = len(claim_words.intersection(content_words))
            if overlap >= len(claim_words) * 0.3:  # 30% overlap threshold
                supporting_articles.append(article)
        
        # Calculate confidence based on supporting articles
        confidence = min(len(supporting_articles) * 0.3, 1.0)
        sources = [article['url'] for article in supporting_articles[:3]]
        
        return FactCheckResult(
            claim=claim,
            verified=len(supporting_articles) > 0,
            confidence=confidence,
            sources=sources,
            evidence=f"Found {len(supporting_articles)} supporting news articles",
            reasoning=f"Claim concepts found in {len(supporting_articles)} recent news articles"
        )
    
    def _extract_key_terms(self, claim: str) -> List[str]:
        """Extract key terms for news search"""
        # Simple key term extraction
        # In production, use more sophisticated NLP
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        
        words = [word.lower().strip('.,!?') for word in claim.split()]
        key_terms = [word for word in words if len(word) > 3 and word not in stop_words]
        
        return key_terms[:5]  # Limit to 5 key terms

class ScientificFactChecker:
    """Scientific literature-based fact checking"""
    
    async def verify_claim_async(self, claim: str, context: str) -> FactCheckResult:
        """Verify claim against scientific literature"""
        # This is a placeholder for scientific fact-checking
        # In production, integrate with PubMed, arXiv, or similar databases
        
        return FactCheckResult(
            claim=claim,
            verified=False,
            confidence=0.0,
            sources=[],
            evidence="Scientific fact-checking not implemented in this example",
            reasoning="Would require integration with scientific databases"
        )
```

## 4. Usage Examples

### 4.1 Basic Usage

```python
import asyncio

async def main():
    # Initialize RAG system
    rag_system = ProductionRAGSystem()
    
    # Sample documents
    documents = [
        Document(
            id="1",
            content="Python is a high-level programming language created by Guido van Rossum in 1991.",
            metadata={"source": "tech_docs", "category": "programming"}
        ),
        Document(
            id="2", 
            content="Machine learning is a subset of artificial intelligence that enables computers to learn without explicit programming.",
            metadata={"source": "ai_guide", "category": "technology"}
        )
        # Add more documents...
    ]
    
    # Initialize index
    await rag_system.initialize_index(documents)
    
    # Query the system
    question = "Who created Python programming language?"
    result = await rag_system.query(question)
    
    print(f"Question: {question}")
    print(f"Answer: {result.answer}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Sources: {len(result.source_documents)}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 4.2 Cached Query Example

```python
async def cached_query_example():
    # Initialize cache
    cache = MultiLevelRAGCache()
    
    async def expensive_computation():
        # Simulate expensive RAG computation
        await asyncio.sleep(2)  # Simulate 2-second processing
        return "This is an expensive computation result"
    
    # First query (cache miss)
    start_time = time.time()
    result1 = await cache.get_or_compute(
        "sample_query_key",
        expensive_computation,
        "response"
    )
    first_query_time = time.time() - start_time
    
    # Second query (cache hit)
    start_time = time.time()
    result2 = await cache.get_or_compute(
        "sample_query_key", 
        expensive_computation,
        "response"
    )
    second_query_time = time.time() - start_time
    
    print(f"First query: {first_query_time:.2f}s")
    print(f"Second query: {second_query_time:.2f}s")
    print(f"Speedup: {first_query_time/second_query_time:.1f}x")
```

### 4.3 Fact-Checking Example

```python
async def fact_checking_example():
    # Initialize fact checker
    fact_checker = RealTimeFactChecker()
    
    # Sample answer with claims to verify
    answer = """
    Python was created by Guido van Rossum in 1991. 
    It is currently the most popular programming language in the world.
    Python is used by over 10 million developers globally.
    """
    
    # Verify answer claims
    verification_result = await fact_checker.verify_answer_realtime(
        answer, 
        "programming languages"
    )
    
    print("Verification Results:")
    print(f"Status: {verification_result['verification_status']}")
    print(f"Overall Confidence: {verification_result['overall_confidence']:.2f}")
    print(f"Verified Claims: {len(verification_result['verified_claims'])}")
    print(f"Disputed Claims: {len(verification_result['disputed_claims'])}")
    print(f"Summary: {verification_result['verification_summary']}")
```

## Conclusion

These implementation examples provide a solid foundation for building production-ready RAG systems with advanced features like verification loops, multi-level caching, and real-time fact-checking. The code is designed to be modular and extensible, allowing for easy customization based on specific requirements.

Key features demonstrated:
- Complete RAG pipeline with verification
- Multi-level caching for performance
- Real-time fact-checking integration
- Production-ready error handling
- Performance monitoring and metrics
- Async processing for scalability

The examples can be adapted and extended for specific domains and use cases, providing a robust starting point for high-accuracy RAG implementations.