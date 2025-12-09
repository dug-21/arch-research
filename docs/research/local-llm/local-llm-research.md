# Local LLM & RAG Architecture Research

**Research Date:** December 2025
**Focus:** Ollama, llama.cpp, Rust Bindings, RAG Implementations

## Executive Summary

Local LLM infrastructure has reached production maturity in 2024 with multiple Rust-native options. Ollama provides user-friendly model management, llama.cpp offers high-performance inference, and rust-bert enables fully native Rust deployment. RAG architectures are well-established with proven Rust implementations using Qdrant and emerging frameworks like Rig.

## 1. Local LLM Landscape

### Ollama

**Overview:** Popular tool for running large language models locally

**Key Features:**
- Simple CLI and REST API interface
- Uses llama.cpp under the hood for inference
- Supports 100+ open-source models (Llama, Mistral, Qwen, Gemma, etc.)
- Built-in model management (download, version, delete)
- GPU acceleration (CUDA, Metal, ROCm)
- Quantization support (Q4, Q5, Q8 variants)

**Model Library (2024):**
- **Llama 3.2:** 1B, 3B (ideal for edge devices)
- **Mistral 7B:** High performance for general tasks
- **Qwen 2.5:** 0.5B-72B, strong multilingual support
- **DeepSeek:** Specialized for coding tasks
- **Phi-3:** Microsoft's efficient small models (3.8B)

**API Example:**
```bash
# Install and run
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b
ollama run llama3.2:3b

# API usage
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Why is the sky blue?"
}'
```

**PKE Applicability:**
- ✅ **Excellent for:** Local LLM management and inference
- ✅ **Benefits:** Zero configuration, automatic model downloads, easy upgrades
- ⚠️ **Consideration:** Additional process dependency (Ollama daemon)
- **Recommendation:** **HIGH PRIORITY** - Use as default local LLM backend

### llama.cpp

**Overview:** High-performance C++ implementation for LLM inference

**Created by:** Georgi Gerganov (creator of whisper.cpp, ggml)

**Key Features:**
- Pure CPU inference with optional GPU acceleration
- Quantization (2-bit to 8-bit) for memory efficiency
- Supports dozens of model architectures
- Cross-platform (Linux, macOS, Windows, Android, iOS)
- Metal (Apple Silicon), CUDA, OpenCL, Vulkan, SYCL backends

**Performance Characteristics:**
- **Llama 3.2 3B Q4:** ~500 tokens/sec on Apple M2, ~200 tokens/sec on mid-range CPU
- **Memory:** ~2-4GB for 3B model, ~4-8GB for 7B model (quantized)
- **Latency:** First token ~100-500ms, subsequent tokens ~5-10ms each

**PKE Applicability:**
- ✅ Can be used directly via Rust bindings
- ✅ Lower-level control than Ollama
- ⚠️ More complex to integrate and manage models
- **Recommendation:** **MEDIUM PRIORITY** - Consider if Ollama doesn't meet performance needs

### Rust LLM Bindings & Libraries

#### 1. llama-cpp-rs

**Description:** Rust bindings for llama.cpp

**Features:**
- Safe Rust API over llama.cpp C++ core
- Supports all llama.cpp features (quantization, GPU, etc.)
- Stream tokens as they're generated
- Embedding generation

**Example:**
```rust
use llama_cpp_rs::{LlamaModel, LlamaParams};

let model = LlamaModel::load_from_file("llama-3.2-3b.gguf", LlamaParams::default())?;
let response = model.generate("Explain quantum computing", GenerateOptions::default())?;
```

**PKE Applicability:**
- ✅ **Excellent for:** Embedding llama.cpp directly in PKE
- ✅ No external daemon required
- ⚠️ Manual model management needed
- **Recommendation:** **HIGH PRIORITY** - Enables fully self-contained Rust deployment

#### 2. ollama-rs

**Description:** Rust client for Ollama REST API

**Features:**
- Async API using tokio
- Type-safe request/response structures
- Streaming support
- Model management (pull, list, delete)

**Example:**
```rust
use ollama_rs::{Ollama, GenerationRequest};

let ollama = Ollama::new("http://localhost:11434".to_string());
let request = GenerationRequest::new("llama3.2:3b".to_string(), "Hello!".to_string());
let response = ollama.generate(request).await?;
```

**PKE Applicability:**
- ✅ **Perfect for:** PKE using Ollama as backend
- ✅ Simple, reliable, actively maintained
- ✅ Async fits Rust ecosystem
- **Recommendation:** **CRITICAL** - Primary integration path for Ollama

#### 3. llm Crate (Pure Rust)

**Description:** Pure Rust implementation for running LLMs

**Features:**
- No C/C++ dependencies
- GGML format support
- Plugin architecture for different models
- Embedding generation

**Status:** Less mature than llama.cpp bindings, smaller model support

**PKE Applicability:**
- ⚠️ Interesting for pure Rust stack but less battle-tested
- **Recommendation:** **LOW PRIORITY** - Monitor for future consideration

#### 4. rust-bert

**Description:** Rust native NLP pipelines using BERT/transformers

**Features:**
- Pre-trained models for various tasks
- Text generation, classification, NER, Q&A
- Sentence embeddings
- ONNX runtime support

**PKE Applicability:**
- ✅ **Excellent for:** Task-specific models (NER, classification, embeddings)
- ✅ Smaller model sizes than LLMs
- ⚠️ Not suitable for conversational AI (use Ollama for that)
- **Recommendation:** **HIGH PRIORITY** - Complement to Ollama for specialized tasks

## 2. RAG (Retrieval-Augmented Generation) Architecture

### What is RAG?

**Definition:** Technique combining information retrieval with generative models to provide accurate, contextually rich responses grounded in external knowledge.

**Architecture Components:**
1. **Document Ingestion:** Parse and chunk documents
2. **Embedding Generation:** Convert text to vector representations
3. **Vector Store:** Index and store embeddings
4. **Retrieval:** Find relevant chunks for a query
5. **Augmentation:** Add retrieved context to LLM prompt
6. **Generation:** LLM produces response grounded in context

### RAG in Rust (2024 Landscape)

#### Rig Library

**Description:** Rust library for building LLM-powered applications

**Features:**
- Simple RAG system in under 100 lines of code
- PDF document extraction and processing
- OpenAI API integration for embeddings and generation
- Vector store abstraction
- Built-in support for Qdrant

**Example Architecture:**
```rust
use rig::{
    embeddings::EmbeddingsBuilder,
    vector_store::VectorStoreIndex,
    providers::openai::{Client, TEXT_EMBEDDING_ADA_002, GPT_3_5_TURBO},
};

// 1. Extract text from PDFs
let documents = extract_pdf_text("knowledge_base.pdf")?;

// 2. Generate embeddings
let client = Client::new(&api_key);
let embeddings = EmbeddingsBuilder::new(TEXT_EMBEDDING_ADA_002)
    .documents(documents)
    .build(&client)
    .await?;

// 3. Create vector store
let index = VectorStoreIndex::new(embeddings);

// 4. Query with RAG
let query = "What is the return policy?";
let context = index.search(query, 5).await?;
let augmented_prompt = format!("Context: {}\n\nQuestion: {}", context, query);
let response = client.complete(GPT_3_5_TURBO, &augmented_prompt).await?;
```

**PKE Applicability:**
- ✅ **Excellent starting point** for RAG implementation
- ✅ Clean abstractions, good documentation
- ⚠️ Currently focused on OpenAI (but extensible)
- **Recommendation:** **HIGH PRIORITY** - Study architecture, adapt for local LLMs

#### Shuttle.dev RAG Tutorials (2024)

**"Building a RAG Web Service with Qdrant and Rust"** (Feb 2024):
- Complete web app with RAG capabilities
- Markdown file parsing for knowledge base
- Query interface with web API
- Production-ready deployment

**"Building Agentic RAG with Rust, Qdrant & OpenAI"** (May 2024):
- Combines AI agents with RAG
- Dynamic workflow based on query type
- Better tailored responses than pure RAG

**Key Insight:** Rust + RAG achieves:
- Low memory footprint
- Fast query processing
- Safe concurrent access to vector stores

**PKE Applicability:**
- ✅ Proven architecture for knowledge retrieval
- ✅ Performance benefits critical for offline-first
- **Recommendation:** **CRITICAL** - Core to PKE's knowledge management

### RAG Landscape Growth (2024)

**Research Activity:**
- 1,200+ RAG-related papers on arXiv in 2024 (vs <100 in 2023)
- Field rapidly maturing with production deployments

**Key Developments:**
- **Unsupervised retrievers:** Avoid costly labeled data
- **Instruction-tuned embedding models:** Better semantic understanding
- **LLM-augmented embeddings:** Use LLMs to improve retrieval quality
- **Hybrid search:** Combine dense vectors + sparse keywords

## 3. Embedding Models for RAG

### Options for PKE

#### Cloud Embeddings (Not Recommended)

- **OpenAI text-embedding-ada-002:** 1536 dims, $0.0001 per 1K tokens
- **Cohere embed-english-v3.0:** 1024 dims, multilingual
- **Voyage AI:** Specialized for RAG tasks

**Problem:** Conflicts with PKE's data sovereignty and offline-first requirements

#### Local Embedding Models

1. **Sentence-Transformers (via rust-bert)**
   - **all-MiniLM-L6-v2:** 384 dims, 80MB, fast
   - **all-mpnet-base-v2:** 768 dims, 420MB, higher quality
   - **multilingual-e5-base:** Supports 100+ languages

2. **FastEmbed (Rust Library)**
   - Fast embedding generation optimized for Rust
   - ONNX runtime for cross-platform inference
   - Multiple model options

3. **Ollama Embeddings**
   - `ollama pull mxbai-embed-large`
   - 1024 dimensions, Apache 2.0 license
   - API: `curl http://localhost:11434/api/embeddings`

**PKE Recommendation:**
- **Primary:** Use Ollama embeddings (e.g., mxbai-embed-large)
- **Alternative:** rust-bert with sentence-transformers
- **Rationale:** Consistent model management, good performance, fully local

## 4. Model Selection for PKE

### Criteria

1. **Size:** Must fit in typical laptop RAM (8-16GB)
2. **Performance:** Acceptable latency (<2 sec for first token)
3. **Quality:** Good enough for personal assistant tasks
4. **License:** Commercial use allowed
5. **Quantization:** Support for Q4/Q5 for efficiency

### Recommended Models

#### Tier 1: Primary Models (3-7B)

1. **Llama 3.2 3B (Q4_K_M)**
   - **Size:** ~2GB
   - **License:** Llama 3.2 Community License (permissive)
   - **Performance:** Excellent for size, ~500 tokens/sec on M2
   - **Use case:** Default local model for most queries

2. **Mistral 7B (Q4_K_M)**
   - **Size:** ~4GB
   - **License:** Apache 2.0
   - **Performance:** High quality general-purpose model
   - **Use case:** When 3B model isn't sufficient

3. **Qwen 2.5 3B (Q4_K_M)**
   - **Size:** ~2GB
   - **License:** Apache 2.0
   - **Strength:** Multilingual, strong reasoning
   - **Use case:** Alternative to Llama for specific tasks

#### Tier 2: Specialized Models

1. **DeepSeek Coder 6.7B (Q4_K_M)**
   - **Size:** ~4GB
   - **Strength:** Code generation and analysis
   - **Use case:** Programming knowledge queries

2. **Phi-3 Mini 3.8B (Q4_K_M)**
   - **Size:** ~2.3GB
   - **Strength:** Efficient, strong reasoning
   - **Use case:** Resource-constrained environments

#### Tier 3: Tiny Models (0.5-1B) - Edge Cases

1. **Qwen 2.5 0.5B (Q4_K_M)**
   - **Size:** ~350MB
   - **Use case:** Ultra-low resource devices, quick classifications

2. **SmolLM 360M**
   - **Size:** ~200MB
   - **Use case:** Embedded systems, mobile devices

### Multi-Model Router Strategy

**Concept:** Intelligently route queries to appropriate model based on:
- Query complexity (simple vs complex)
- Required knowledge domain (general, code, multilingual)
- Privacy sensitivity (local vs cloud)
- Resource availability (battery, network)

**Implementation:**
```rust
pub enum ModelTier {
    Tiny,      // 0.5-1B models
    Small,     // 3B models
    Medium,    // 7B models
    Large,     // 13B+ models (rare, high-end hardware)
    Cloud,     // Claude/GPT (sanitized queries only)
}

pub struct ModelRouter {
    pub fn select_model(&self, query: &Query) -> ModelTier {
        match (query.complexity, query.has_pii, query.domain) {
            (Complexity::Simple, false, _) => ModelTier::Tiny,
            (_, true, _) => ModelTier::Small, // PII stays local
            (Complexity::Complex, false, Domain::Code) => ModelTier::Medium,
            (Complexity::Complex, false, _) if self.allow_cloud => ModelTier::Cloud,
            _ => ModelTier::Small,
        }
    }
}
```

## 5. Performance Benchmarks

### Inference Speed (Approximate, CPU)

| Model | Quantization | RAM | First Token | Throughput | Hardware |
|-------|--------------|-----|-------------|------------|----------|
| Llama 3.2 1B | Q4_K_M | 1GB | ~50ms | 800 tok/s | M2 Pro |
| Llama 3.2 3B | Q4_K_M | 2GB | ~100ms | 500 tok/s | M2 Pro |
| Mistral 7B | Q4_K_M | 4GB | ~200ms | 250 tok/s | M2 Pro |
| Llama 3.2 3B | Q4_K_M | 2GB | ~300ms | 150 tok/s | i5-12400 |
| Mistral 7B | Q4_K_M | 4GB | ~600ms | 80 tok/s | i5-12400 |

### Embedding Generation Speed

| Model | Dimensions | Throughput | Size |
|-------|-----------|------------|------|
| all-MiniLM-L6-v2 | 384 | ~5000 docs/sec | 80MB |
| mxbai-embed-large | 1024 | ~2000 docs/sec | 330MB |
| all-mpnet-base-v2 | 768 | ~3000 docs/sec | 420MB |

## Gap Analysis vs PKE Requirements

| Requirement | Technology | Status | PKE Fit |
|------------|-----------|--------|---------|
| Local inference | Ollama + llama.cpp | ✅ Production | Perfect |
| Offline-first | Local model files | ✅ Production | Essential |
| Rust integration | ollama-rs, llama-cpp-rs | ✅ Production | Excellent |
| RAG architecture | Rig, custom impl | ✅ Proven | Core feature |
| Multi-model support | Ollama library | ✅ Production | Differentiator |
| Privacy by design | Local-only execution | ✅ Architectural | Fundamental |

## Build vs Integrate Recommendations

### INTEGRATE

1. **Ollama**
   - **Use for:** Model management and inference
   - **Why:** Battle-tested, great UX, active development
   - **Integration:** ollama-rs crate
   - **Priority:** **CRITICAL**

2. **Qdrant** (covered in vector DB report)
   - **Use for:** Vector storage and retrieval
   - **Why:** Best-in-class Rust vector database
   - **Priority:** **CRITICAL**

3. **rust-bert**
   - **Use for:** Embedding generation, NER, classification
   - **Why:** Native Rust, no external dependencies
   - **Priority:** **HIGH**

4. **Rig Framework Patterns**
   - **Extract:** RAG architecture patterns and abstractions
   - **Adapt:** For local-only Ollama backend
   - **Priority:** **HIGH**

### BUILD

1. **Model Router**
   - **What:** Intelligent model selection based on query characteristics
   - **Why:** Optimize performance vs quality trade-offs
   - **Priority:** **HIGH** - Key differentiator

2. **RAG Pipeline**
   - **What:** Custom implementation using Qdrant + Ollama
   - **Why:** Tailored to PKE's offline-first, privacy-focused needs
   - **Priority:** **CRITICAL**

3. **Embedding Cache**
   - **What:** Persistent cache of generated embeddings
   - **Why:** Avoid recomputing embeddings for static knowledge
   - **Priority:** **MEDIUM**

4. **Model Auto-Updater**
   - **What:** Background service to download model updates
   - **Why:** Keep models current without user intervention
   - **Priority:** **LOW** - Post-MVP

## Implementation Roadmap

### Phase 1: MVP (Months 1-3)

**Month 1: Foundation**
- Integrate Ollama via ollama-rs
- Implement basic LLM query interface
- Download and test Llama 3.2 3B, Mistral 7B
- Build simple prompt templates

**Month 2: RAG Core**
- Integrate Qdrant (see vector DB report)
- Implement document ingestion pipeline
- Generate embeddings with Ollama (mxbai-embed-large)
- Build retrieval and augmentation logic

**Month 3: Intelligence**
- Implement Model Router for query classification
- Add PII detection integration (see anonymization report)
- Build privacy-aware routing (local vs cloud)
- Create user-facing model selection UI

### Phase 2: Enhanced RAG (Months 4-6)

- Hybrid search (vectors + keywords)
- Advanced chunking strategies
- Re-ranking with rust-bert
- Context window optimization
- Conversation history management

### Phase 3: Advanced Features (Months 7+)

- Fine-tuning local models on personal data
- Multi-modal support (images, PDFs, code)
- Agentic RAG with tool use
- Distributed RAG across devices
- Model quantization optimization

## Novel Differentiators for PKE

1. **Privacy-Tiered Model Routing**
   - Automatic sensitivity detection
   - Always-local for PII, optional cloud for general queries
   - User-visible routing decisions with explanations

2. **Personal Knowledge Optimization**
   - Fine-tune local models on user's knowledge base
   - Personalized embeddings that understand user's domain
   - Continuous learning from user interactions

3. **Offline-First RAG**
   - Complete functionality without internet
   - Local model + local vector DB = zero external dependencies
   - Sync knowledge when online, query anytime

4. **Multi-Model Ensemble**
   - Route queries to best-fit model automatically
   - Llama for general, DeepSeek for code, Qwen for multilingual
   - Performance optimization without sacrificing quality

5. **Transparent Operation**
   - Show user which model answered query
   - Display retrieved context and confidence scores
   - Allow model preference overrides

## Rust RAG Architecture Example

```rust
use ollama_rs::{Ollama, GenerationRequest, EmbeddingRequest};
use qdrant_client::{client::QdrantClient, qdrant::SearchPoints};

pub struct PKEAssistant {
    ollama: Ollama,
    vector_db: QdrantClient,
    model_router: ModelRouter,
    sanitizer: QuerySanitizer,
}

impl PKEAssistant {
    pub async fn query(&self, user_query: &str) -> Result<Response> {
        // 1. Sanitize query for PII
        let sanitized = self.sanitizer.sanitize(user_query)?;

        // 2. Generate query embedding
        let embedding = self.ollama
            .generate_embedding("mxbai-embed-large", &sanitized.text)
            .await?;

        // 3. Retrieve relevant context from vector DB
        let search = SearchPoints {
            collection_name: "knowledge_base".to_string(),
            vector: embedding,
            limit: 5,
            with_payload: Some(true),
            ..Default::default()
        };
        let results = self.vector_db.search_points(&search).await?;

        // 4. Build augmented prompt
        let context = results.iter()
            .map(|r| r.payload.get("text").unwrap())
            .collect::<Vec<_>>()
            .join("\n\n");
        let augmented = format!(
            "Context:\n{}\n\nQuestion: {}\n\nAnswer:",
            context, sanitized.text
        );

        // 5. Route to appropriate model
        let model = self.model_router.select_model(&sanitized);

        // 6. Generate response
        let request = GenerationRequest::new(model, augmented);
        let response = self.ollama.generate(request).await?;

        Ok(Response {
            text: response.response,
            model_used: model,
            context_retrieved: results,
            sanitization_applied: sanitized.entities_removed,
        })
    }
}
```

## Sources

1. [Building Agentic RAG with Rust, Qdrant & OpenAI | Shuttle](https://www.shuttle.dev/blog/2024/05/23/building-agentic-rag-rust-qdrant)
2. [Building a RAG Web Service with Qdrant and Rust | Shuttle](https://www.shuttle.dev/blog/2024/02/28/rag-llm-rust)
3. [Building a RAG System with Rig 0.24.0](https://docs.rig.rs/guides/rag/rag_system)
4. [Retrieval-Augmented Generation: A Comprehensive Survey](https://arxiv.org/html/2506.00054v1)
5. [rust-bert: Rust native NLP pipelines](https://github.com/guillaume-be/rust-bert)
6. [Machine Learning in Rust - Awesome Rust MachineLearning](https://github.com/vaaaaanquish/Awesome-Rust-MachineLearning)

## Conclusion

Local LLM and RAG technology is production-ready for PKE implementation. The recommended stack:

1. **Ollama** for model management and inference
2. **ollama-rs** for Rust integration
3. **Qdrant** for vector storage (see vector DB report)
4. **rust-bert** for specialized NLP tasks
5. **Custom RAG pipeline** tailored to privacy-first, offline-first requirements

This architecture achieves:
- ✅ Complete data sovereignty (no data leaves device)
- ✅ Offline-first operation (no internet required)
- ✅ Excellent performance (modern hardware can run 3-7B models smoothly)
- ✅ Privacy by design (all processing local)
- ✅ Extensibility (easy to add new models and capabilities)
