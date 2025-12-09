# Comprehensive Local LLM Deployment Guide for Privacy-Focused PKE

**Research Date:** December 2025
**Focus:** Production-Ready Local LLM Infrastructure for Personal Knowledge Engine
**Status:** Comprehensive Analysis - All Major Runtimes & Frameworks

---

## Executive Summary

This comprehensive guide provides production-ready recommendations for deploying local LLMs in a privacy-focused Personal Knowledge Engine (PKE). Based on extensive research of 2024-2025 developments, we cover:

- **5 Major LLM Runtimes**: Ollama, llama.cpp, vLLM, ExLLaMA, MLX
- **6 Rust-Native Frameworks**: candle, burn, tract, llama-cpp-rs, ollama-rs, rust-bert
- **3 Hardware Tiers**: 8GB minimum, 32GB optimal, Apple Silicon path
- **Advanced RAG**: Chunk optimization, hybrid search, reranking
- **Intelligent Routing**: PII detection, local vs cloud decision-making

**Key Finding**: Local LLM infrastructure is production-ready for PKE with multiple mature options across all components.

---

## Table of Contents

1. [Local LLM Runtimes](#1-local-llm-runtimes)
2. [Rust-Native LLM Integration](#2-rust-native-llm-integration)
3. [Model Selection for Privacy RAG](#3-model-selection-for-privacy-rag)
4. [Intelligent Routing Architecture](#4-intelligent-routing-architecture)
5. [RAG Architecture Best Practices](#5-rag-architecture-best-practices)
6. [Hardware-Specific Recommendations](#6-hardware-specific-recommendations)
7. [Production Implementation Roadmap](#7-production-implementation-roadmap)
8. [Sources](#sources)

---

## 1. Local LLM Runtimes

### 1.1 Ollama - User-Friendly Model Management ⭐⭐⭐⭐⭐

**Overview:** Industry-leading tool for running LLMs locally with zero-configuration setup.

**Key Features:**
- Uses llama.cpp under the hood for high-performance inference
- 100+ pre-configured models (Llama, Mistral, Qwen, Gemma, DeepSeek, Phi)
- Built-in model management (download, version, delete)
- REST API on `localhost:11434`
- GPU acceleration (CUDA, Metal, ROCm)
- Quantization support (Q4, Q5, Q8 variants)

**API Example:**
```bash
# Install and run
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b
ollama run llama3.2:3b

# API usage (REST)
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Why is the sky blue?"
}'

# Embeddings API
curl http://localhost:11434/api/embeddings -d '{
  "model": "mxbai-embed-large",
  "prompt": "Represent this sentence for retrieval"
}'
```

**Performance Characteristics:**
- Llama 3.2 3B Q4: ~500 tokens/sec on Apple M2, ~200 tokens/sec on mid-range CPU
- Memory: ~2-4GB for 3B model, ~4-8GB for 7B model (quantized)
- First token latency: ~100-500ms
- Subsequent tokens: ~5-10ms each

**PKE Applicability:**
- ✅ **PRIMARY RECOMMENDATION**: Zero-config, production-ready
- ✅ **Perfect for MVP**: Handles model downloads, updates automatically
- ✅ **Rust Integration**: Via ollama-rs crate (see section 2.1)
- ⚠️ **Trade-off**: Requires daemon process (small overhead)

**Verdict:** **CRITICAL PRIORITY** - Use as default local LLM backend for PKE.

---

### 1.2 llama.cpp - High-Performance C++ Inference ⭐⭐⭐⭐

**Overview:** Industry-standard C++ implementation for LLM inference (by Georgi Gerganov, creator of whisper.cpp, ggml).

**Key Features:**
- Pure CPU inference with optional GPU acceleration
- GGUF format support (2-bit to 8-bit quantization)
- Cross-platform (Linux, macOS, Windows, Android, iOS)
- Backend support: Metal (Apple Silicon), CUDA, OpenCL, Vulkan, SYCL
- Dozens of model architectures supported

**Performance:**
- Same performance as Ollama (Ollama uses llama.cpp internally)
- Direct control over inference parameters
- Memory-efficient quantization

**PKE Applicability:**
- ✅ **Alternative to Ollama**: Lower-level control if needed
- ✅ **Rust Integration**: Via llama-cpp-rs (see section 2.2)
- ⚠️ **Complexity**: Manual model management and format conversion
- **Recommendation:** **MEDIUM PRIORITY** - Consider if Ollama doesn't meet specific needs

---

### 1.3 vLLM - High-Throughput Serving Engine ⭐⭐⭐⭐

**Overview:** Production-grade inference and serving engine from UC Berkeley, now part of PyTorch Foundation.

**Key Features:**
- PagedAttention algorithm for memory efficiency
- Continuous batching for high throughput
- OpenAI API-compatible endpoints
- Quantization: FP8+INT8, GPTQ, AWQ, GGUF, bitsandbytes
- Hardware support: NVIDIA, AMD, Intel CPUs/GPUs/XPUs, TPU

**2025 Developments:**
- **vLLM V1 Alpha** (Jan 2025): 1.7x speedup, zero-overhead prefix caching
- **PyTorch Foundation** (May 2025): Now hosted project with enterprise backing
- Powers production systems (Amazon Rufus, LinkedIn AI features)

**Deployment Options:**
```bash
# Docker deployment
docker run --gpus all -p 8000:8000 vllm/vllm-openai:latest \
  --model meta-llama/Llama-3.2-3B

# CPU-only mode (no GPU required)
docker run -p 8000:8000 vllm/vllm-openai:latest \
  --model meta-llama/Llama-3.2-3B --cpu-only

# BentoML integration
bentoml serve vllm-service:latest
```

**Performance Characteristics:**
- Best-in-class throughput for batch processing
- Excellent for high-volume API serving
- 16GB VRAM minimum recommended for GPU mode
- CPU mode works but significantly slower

**PKE Applicability:**
- ⚠️ **Overkill for single-user**: Designed for multi-user serving
- ✅ **Future consideration**: If PKE evolves to multi-user/server mode
- ❌ **Not for MVP**: Complexity outweighs benefits for personal use
- **Recommendation:** **LOW PRIORITY** - Monitor for future server-based deployments

**Verdict:** Excellent for production API serving, but unnecessary complexity for single-user PKE.

---

### 1.4 ExLLaMA / ExLLaMAv2 - Optimized GPTQ Inference ⭐⭐⭐⭐

**Overview:** Blazingly fast inference library optimized for GPTQ and EXL2 quantization on consumer GPUs.

**Key Innovations:**

#### EXL2 Quantization Format
- Based on GPTQ with mixed-precision support
- Supports 2, 3, 4, 5, 6, 8-bit quantization
- **Mixed precision within model**: Preserve important weights with more bits
- Achieve any average bitrate between 2-8 bits per weight

**Performance Comparison:**
```
Speed Benchmarks (13B model on T4 GPU):
- ExLlamaV2 (GPTQ): 56.44 tokens/sec (fastest)
- ExLlamaV1: 49.8 tokens/sec (13% slower)
- llama.cpp: ~45 tokens/sec
- Standard GPTQ: ~40 tokens/sec
```

**Quality vs Size Trade-offs:**
```
llama-2-13b Examples:
- EXL2-4.250b: Lower perplexity than GPTQ-4bit-128g, smaller on disk, more VRAM
- EXL2-4.650b: Lower perplexity than GPTQ-4bit-32g, smaller on disk, more VRAM
```

**Advanced Features (2024):**
- Paged attention via Flash Attention 2.5.7+
- Dynamic batching for multi-query efficiency
- Smart prompt caching (reduces repeated computation)
- K/V cache deduplication
- Simplified API for easier integration

**Integration:**
- Used by Aphrodite Engine for boosted throughput
- Supports 2, 3, 4, 8-bit quantization
- Python-based (no direct Rust bindings currently)

**PKE Applicability:**
- ✅ **GPU users**: Best speed for NVIDIA GPU owners
- ✅ **Quality-conscious**: EXL2 mixed precision preserves model quality
- ⚠️ **Python dependency**: Not native Rust (limits PKE integration)
- ❌ **CPU-only users**: Designed for GPU, minimal CPU benefit
- **Recommendation:** **MEDIUM PRIORITY** - Evaluate for GPU-accelerated PKE variant

**Verdict:** Excellent for GPU users wanting maximum speed, but Python dependency limits Rust ecosystem integration.

---

### 1.5 MLX - Apple Silicon Native Framework ⭐⭐⭐⭐⭐

**Overview:** Apple's ML framework optimized for unified memory architecture of Apple Silicon.

**Key Features:**
- Native optimization for M-series chips (M1, M2, M3, M4, M5)
- Unified memory architecture (CPU/GPU share memory)
- Neural Accelerators support (M5 chips)
- Array framework similar to NumPy/PyTorch
- Designed for on-device inference and experimentation

**M5 Performance Benchmarks (Nov 2025):**
```
M5 vs M4 Improvements:
- Time-to-first-token: Up to 4x faster (via GPU Neural Accelerators)
- Token generation: 19-27% faster (thanks to 28% higher memory bandwidth)
- Memory bandwidth: 153GB/s (M5) vs 120GB/s (M4)
- Image generation (FLUX-dev 12B): 3.8x faster on M5 vs M4
```

**Comparative Performance (Oct 2025 Study - M2 Ultra, 192GB RAM):**
```
Framework Comparison on Apple Silicon:
- MLX: Highest sustained generation throughput
- MLC-LLM: Lower time-to-first-token (TTFT), better inference features
- llama.cpp: Excellent general performance
- Ollama: Best ease of use (uses llama.cpp)
- PyTorch MPS: Slowest, experimental
```

**Unified Memory Advantage:**
- Run 670B parameter models on M3 Ultra with 512GB RAM (DeepSeek AI)
- Zero-copy operations between CPU/GPU
- No VRAM limitations (uses system RAM)

**MLX vs CUDA:**
- Significant performance gap vs NVIDIA for training workloads
- Competitive for inference on consumer hardware
- CUDA still preferred for performance-critical training
- MLX compelling for on-device inference and experimentation

**Benchmarks (M1 Max - Mistral 7B Q4):**
```
Framework Speed Comparison:
1. llama.cpp: Fastest
2. Candle Rust: Close second
3. MLX: Trailing, but improving rapidly
```

**PKE Applicability:**
- ✅ **Apple Silicon users**: CRITICAL PRIORITY
- ✅ **Unified memory**: Leverage full system RAM for large models
- ✅ **M5 users**: Neural Accelerators provide significant speedup
- ⚠️ **Apple-only**: No cross-platform portability
- **Recommendation:** **CRITICAL for Apple users** - Primary runtime for M-series hardware

**Verdict:** Best-in-class for Apple Silicon, especially M4/M5 with Neural Accelerators.

---

### Runtime Comparison Matrix

| Runtime | Speed | Ease of Use | Rust Native | Cross-Platform | PKE Priority |
|---------|-------|-------------|-------------|----------------|--------------|
| **Ollama** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ (via ollama-rs) | ✅ | **CRITICAL** |
| **llama.cpp** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ❌ (via llama-cpp-rs) | ✅ | **MEDIUM** |
| **vLLM** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ❌ | ✅ | **LOW** |
| **ExLLaMA** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ❌ | ❌ (GPU only) | **MEDIUM** |
| **MLX** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ | ❌ (Apple only) | **CRITICAL (Apple)** |

---

## 2. Rust-Native LLM Integration

### 2.1 ollama-rs - Rust Client for Ollama ⭐⭐⭐⭐⭐

**Description:** Official Rust client for Ollama REST API.

**Features:**
- Async API using tokio
- Type-safe request/response structures
- Streaming support for real-time token generation
- Model management (pull, list, delete)
- Embeddings generation

**Example:**
```rust
use ollama_rs::{Ollama, GenerationRequest, EmbeddingRequest};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let ollama = Ollama::new("http://localhost:11434".to_string());

    // Generate text
    let request = GenerationRequest::new(
        "llama3.2:3b".to_string(),
        "Explain quantum computing in simple terms".to_string()
    );
    let response = ollama.generate(request).await?;
    println!("Response: {}", response.response);

    // Generate embeddings for RAG
    let embed_request = EmbeddingRequest::new(
        "mxbai-embed-large".to_string(),
        "Represent this sentence for retrieval".to_string()
    );
    let embeddings = ollama.generate_embeddings(embed_request).await?;
    println!("Embedding dimensions: {}", embeddings.embedding.len());

    Ok(())
}
```

**PKE Applicability:**
- ✅ **PRIMARY INTEGRATION**: Simple, reliable, actively maintained
- ✅ **Perfect async fit**: Works seamlessly with Rust async ecosystem
- ✅ **Production-ready**: Used in production Rust applications
- **Recommendation:** **CRITICAL** - Primary integration path for Ollama in PKE

---

### 2.2 llama-cpp-rs - Rust Bindings for llama.cpp ⭐⭐⭐⭐

**Description:** Safe Rust bindings over llama.cpp C++ core.

**Features:**
- Direct access to all llama.cpp features
- Supports quantization, GPU acceleration
- Stream tokens as generated
- Embedding generation
- No daemon dependency (self-contained)

**Example:**
```rust
use llama_cpp_rs::{LlamaModel, LlamaParams, GenerateOptions};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Load model
    let model = LlamaModel::load_from_file(
        "models/llama-3.2-3b-Q4_K_M.gguf",
        LlamaParams::default()
    )?;

    // Generate response
    let response = model.generate(
        "Explain quantum computing",
        GenerateOptions {
            max_tokens: 150,
            temperature: 0.7,
            ..Default::default()
        }
    )?;

    println!("Generated: {}", response);
    Ok(())
}
```

**PKE Applicability:**
- ✅ **Self-contained**: No external daemon required
- ✅ **Direct control**: Fine-grained control over inference
- ⚠️ **Manual management**: Must handle model downloads/updates
- **Recommendation:** **HIGH PRIORITY** - Enables fully self-contained Rust deployment

---

### 2.3 candle - HuggingFace Rust ML Framework ⭐⭐⭐⭐

**Overview:** Minimalist ML framework for Rust backed by HuggingFace.

**Key Features:**
- PyTorch-like syntax for familiarity
- CPU backend with MKL support (x86) and Accelerate (macOS)
- CUDA backend for GPU efficiency
- WASM support (run models in browser)
- Model training and inference
- Zero Python overhead in production

**Why Candle for PKE?**
- Remove Python from production workloads (no GIL headaches)
- Lightweight binaries for fast deployment
- WASM enables browser-based inference

**Supported Models (LLMs):**
- LLaMA v1, v2, v3 (including SOLAR-10.7B)
- Mistral 7b-v0.1 (general 7B LLM)
- Mixtral 8x7b-v0.1 (sparse MoE)
- StarCoder & StarCoder2 (code generation)
- Qwen1.5 (bilingual English/Chinese)
- RWKV v5/v6 (RNN with transformer performance)

**Beyond LLMs:**
- Stable Diffusion v1.5, v2.1, XL v1.0 (text-to-image)
- Whisper (speech-to-text)
- Vision: DINOv2, EfficientNet, ResNet, ViT, SAM

**Ecosystem Tools:**
- **candle-vllm**: OpenAI-compatible API server for local LLMs
- **candle-lora**: Efficient LoRA fine-tuning support

**Performance Benchmarks (M1 - Mistral 7B Q4):**
```
1. llama.cpp: Fastest
2. Candle Rust: Very close second
3. MLX: Trailing
```

**Getting Started:**
```bash
# Run Mistral model
cargo run --example mistral --release --features cuda \
  -- --prompt 'Write hello world in Rust' \
  --sample-len 150 --quantized
```

**Example Code:**
```rust
use candle::{Tensor, Device};
use candle_transformers::models::llama;

fn main() -> Result<()> {
    let device = Device::cuda_if_available(0)?;

    // Load model
    let model = llama::Llama::load("models/mistral-7b", &device)?;

    // Generate text
    let prompt = "Explain Rust ownership";
    let tokens = model.generate(prompt, 150)?;

    println!("Generated: {}", tokens);
    Ok(())
}
```

**PKE Applicability:**
- ✅ **Pure Rust stack**: No Python dependencies in production
- ✅ **WASM support**: Enable browser-based PKE interface
- ✅ **HuggingFace backing**: Strong ecosystem support
- ⚠️ **Less mature**: Younger than llama.cpp/Ollama
- **Recommendation:** **HIGH PRIORITY** - Excellent for pure Rust architecture

---

### 2.4 burn - Pure Rust Deep Learning Framework ⭐⭐⭐⭐

**Overview:** Next-generation tensor library and deep learning framework designed in Rust.

**Key Features:**
- Backend agnostic (CPU, CUDA, Metal, WGPU, Vulkan, HIP/ROCm)
- Dynamic computation graphs
- Strong type safety (compile-time error catching)
- High performance (matches/exceeds LibTorch in benchmarks)
- Memory safety via Rust ownership
- Composable backends with autodifferentiation and kernel fusion

**2024 Achievements:**
- Performance now matches or surpasses LibTorch
- CUDA, HIP/ROCm, WGPU (WebGPU + Vulkan) backends
- Advanced kernel fusion

**2025 Roadmap:**
- Quantization support (crucial for edge deployment)
- JIT vectorized CPU backend
- FPGA support exploration
- Distributed training infrastructure (Router + HTTP backends)

**Model Import:**
- **ONNX**: Convert TensorFlow/PyTorch models to Rust code
- **PyTorch/Safetensors**: Load weights directly into Burn models
- Enables model reuse with Burn optimizations

**Why Rust for Deep Learning?**
- Zero-cost abstractions for neural network modules
- Fine-grained memory control
- Fast execution with high-level abstractions

**PKE Applicability:**
- ✅ **Future-proof**: Pure Rust, modern architecture
- ✅ **Flexible**: Train custom models on user's personal data
- ✅ **Cross-platform**: Backend flexibility (CPU, GPU, WASM)
- ⚠️ **Emerging**: Newer framework, smaller ecosystem
- **Recommendation:** **MEDIUM PRIORITY** - Monitor for custom model training in Phase 2+

---

### 2.5 tract - ONNX Inference in Rust ⭐⭐⭐⭐

**Overview:** Sonos' neural network inference toolkit for ONNX, NNEF, and TensorFlow.

**Design Philosophy:**
- Embedding-friendly and portable
- Run NN inference on edge, browser, small CPUs
- Convert models to intermediate representation
- Optimize and execute efficiently

**ONNX Support:**
- ~85% of ONNX backend tests pass
- All "real-life" ONNX test suite tests passing:
  - bvlc_alexnet, densenet121, inception_v1/v2
  - resnet50, shufflenet, squeezenet, vgg19, zfnet512
- Missing: Tensor Sequences, Optional Tensors (structural limitation)

**Components:**
- **tract-onnx**: Load and run ONNX networks
- **tract-tensorflow**: TensorFlow 1 network support
- **tract-nnef**: NNEF network support

**Current Status (2024/2025):**
- Rust edition "2024"
- Requires rust-version "1.85"
- Actively developed

**PKE Applicability:**
- ✅ **Model flexibility**: Import ONNX models from any framework
- ✅ **Production-ready**: Used by Sonos in production
- ✅ **Embedded-friendly**: Perfect for offline-first PKE
- ⚠️ **Inference-only**: No training capabilities
- **Recommendation:** **MEDIUM PRIORITY** - Useful for importing pre-trained ONNX models

---

### 2.6 rust-bert - Native NLP Pipelines ⭐⭐⭐⭐

**Description:** Rust native NLP pipelines using BERT/transformers.

**Features:**
- Pre-trained models for various tasks
- Text generation, classification, NER, Q&A
- Sentence embeddings (for RAG)
- ONNX runtime support

**Example:**
```rust
use rust_bert::pipelines::sentence_embeddings::SentenceEmbeddingsBuilder;
use rust_bert::pipelines::ner::NERModel;

fn main() -> Result<()> {
    // Generate embeddings for RAG
    let model = SentenceEmbeddingsBuilder::remote(
        SentenceEmbeddingsModelType::AllMiniLmL6V2
    ).create_model()?;

    let sentences = vec!["This is an example", "This is another example"];
    let embeddings = model.encode(&sentences)?;

    // Named Entity Recognition for PII detection
    let ner_model = NERModel::new(Default::default())?;
    let input = vec!["My name is John Smith and I live in New York"];
    let entities = ner_model.predict(&input);

    Ok(())
}
```

**Available Models:**
- **Embeddings**: all-MiniLM-L6-v2 (384 dims, 80MB), all-mpnet-base-v2 (768 dims, 420MB)
- **NER**: BERT-based models for entity recognition
- **Classification**: Sentiment analysis, text categorization

**PKE Applicability:**
- ✅ **Excellent for specialized tasks**: NER, classification, embeddings
- ✅ **Smaller models**: 80-420MB vs multi-GB LLMs
- ✅ **Perfect complement**: Use with Ollama for task-specific operations
- ⚠️ **Not for conversation**: Use Ollama for general LLM tasks
- **Recommendation:** **HIGH PRIORITY** - Complement to Ollama for PII detection, embeddings

---

### Rust Framework Comparison Matrix

| Framework | Use Case | Maturity | Rust Native | PKE Priority |
|-----------|----------|----------|-------------|--------------|
| **ollama-rs** | LLM client | ⭐⭐⭐⭐⭐ | ✅ | **CRITICAL** |
| **llama-cpp-rs** | LLM embedding | ⭐⭐⭐⭐ | ⚠️ (C++ bindings) | **HIGH** |
| **candle** | Full ML stack | ⭐⭐⭐ | ✅ | **HIGH** |
| **burn** | Training + inference | ⭐⭐⭐ | ✅ | **MEDIUM** |
| **tract** | ONNX inference | ⭐⭐⭐⭐ | ✅ | **MEDIUM** |
| **rust-bert** | NLP tasks | ⭐⭐⭐⭐ | ✅ | **HIGH** |

---

## 3. Model Selection for Privacy RAG

### 3.1 Model Selection Criteria

**Requirements for PKE:**
1. **Size**: Fit in typical laptop RAM (8-32GB)
2. **Performance**: Acceptable latency (<2 sec first token)
3. **Quality**: Good enough for personal assistant tasks
4. **License**: Commercial use allowed
5. **Quantization**: Support Q4/Q5 for efficiency
6. **Privacy**: Can run fully offline

### 3.2 VRAM/RAM Requirements by Model Size

**General Rule:** ~2GB per billion parameters + 20% overhead

**Tier Breakdown:**

#### 8GB RAM/VRAM (Minimum Viable)
```
Recommended Models:
- Llama 3.2 1B Q4: ~1GB, 800 tok/s on M2
- Llama 3.2 3B Q4: ~2GB, 500 tok/s on M2
- Qwen 2.5 3B Q4: ~2GB, strong reasoning
- Phi-3 Mini 3.8B Q4: ~2.3GB, efficient

Capability: ChatGPT-3.5-like performance
Context: 2K-8K tokens
Use case: Basic queries, simple RAG
```

#### 16GB RAM/VRAM (Sweet Spot)
```
Recommended Models:
- Llama 3.2 3B Q4: Full precision, long context
- Mistral 7B Q4: ~4GB, high-quality general purpose
- Qwen 2.5 7B Q4: ~4GB, multilingual
- DeepSeek Coder 6.7B Q4: ~4GB, code-focused

Capability: ChatGPT-3.5+ performance
Context: 8K-32K tokens
Use case: Complex queries, comprehensive RAG
Verdict: Best price-to-performance for most users
```

#### 24GB RAM/VRAM (Professional)
```
Recommended Models:
- Qwen 3 30B MoE Q4: ~16GB, 65K context
- Llama 3.1 30B Q4: ~16GB, dense model
- Mixtral 8x7B Q4: ~24GB, MoE architecture

Capability: ChatGPT-4-like performance
Context: 32K-128K tokens
Use case: Advanced reasoning, large document analysis
Verdict: Best balance for professionals
```

#### 32GB+ RAM/VRAM (Enthusiast)
```
Recommended Models:
- Llama 3.1 70B Q4: ~40GB (needs offloading)
- Qwen 3 14B Q4: Full precision, 131K context
- Qwen 3 32B Q4: 45K context

Capability: Near GPT-4 performance
Context: 45K-147K tokens
Use case: Research, complex analysis, full documents
Verdict: Enthusiast/workstation setups
```

### 3.3 Recommended Model Tiers for PKE

#### Tier 1: Primary Models (3-7B) - Default for PKE

**1. Llama 3.2 3B (Q4_K_M)**
```
Size: ~2GB
License: Llama 3.2 Community License (permissive)
Performance: ~500 tokens/sec on M2, ~200 tokens/sec on mid-range CPU
Strengths: Excellent balance of speed/quality
Use case: Default local model for most queries
PKE Priority: CRITICAL
```

**2. Mistral 7B (Q4_K_M)**
```
Size: ~4GB
License: Apache 2.0
Performance: High-quality general-purpose model
Strengths: Best quality in 7B class
Use case: When 3B model quality isn't sufficient
PKE Priority: HIGH
```

**3. Qwen 2.5 3B (Q4_K_M)**
```
Size: ~2GB
License: Apache 2.0
Strengths: Multilingual, strong reasoning
Use case: Alternative to Llama for specific tasks
PKE Priority: HIGH
```

#### Tier 2: Specialized Models

**1. DeepSeek Coder 6.7B (Q4_K_M)**
```
Size: ~4GB
Strengths: Code generation and analysis
Use case: Programming knowledge queries
PKE Priority: MEDIUM (code-heavy users: HIGH)
```

**2. Phi-3 Mini 3.8B (Q4_K_M)**
```
Size: ~2.3GB
Strengths: Efficient, strong reasoning
Use case: Resource-constrained environments
PKE Priority: MEDIUM
```

#### Tier 3: Embedding Models for RAG

**1. mxbai-embed-large (via Ollama)**
```
Size: 330MB
Dimensions: 1024
Throughput: ~2000 docs/sec
License: Apache 2.0
Recommendation: PRIMARY for PKE embeddings
```

**2. all-MiniLM-L6-v2 (via rust-bert)**
```
Size: 80MB
Dimensions: 384
Throughput: ~5000 docs/sec
Recommendation: Fast alternative, lower quality
```

**3. all-mpnet-base-v2 (via rust-bert)**
```
Size: 420MB
Dimensions: 768
Throughput: ~3000 docs/sec
Recommendation: Higher quality alternative
```

### 3.4 Quantization Impact Analysis

**Quantization Methods:**

| Method | Size Reduction | Quality Impact | Speed Impact | Recommendation |
|--------|----------------|----------------|--------------|----------------|
| **Q8** | 2x | Minimal (~1% perplexity increase) | Fastest | Quality-critical tasks |
| **Q5_K_M** | 3x | Very low (~2% perplexity increase) | Very fast | Balanced default |
| **Q4_K_M** | 4x | Low (~3-5% perplexity increase) | Fast | **PKE Default** |
| **Q4_K_S** | 4.5x | Moderate (~5-7% perplexity increase) | Faster | Space-constrained |
| **Q3_K_M** | 6x | Noticeable (~8-10% perplexity increase) | Very fast | Edge devices |
| **Q2_K** | 8x | Significant (~15%+ perplexity increase) | Extremely fast | Avoid for PKE |

**PKE Recommendation:** Use **Q4_K_M** as default - best quality/size trade-off.

### 3.5 Model Router Strategy

**Concept:** Intelligently route queries to appropriate model based on characteristics.

**Implementation:**
```rust
pub enum ModelTier {
    Tiny,      // 0.5-1B models
    Small,     // 3B models (default)
    Medium,    // 7B models
    Specialized, // Domain-specific (code, multilingual)
    Cloud,     // Claude/GPT (sanitized queries only)
}

pub struct ModelRouter {
    available_memory: usize,
    privacy_mode: PrivacyLevel,
}

impl ModelRouter {
    pub fn select_model(&self, query: &Query) -> ModelSelection {
        // Rule 1: Privacy override
        if query.has_pii || self.privacy_mode == PrivacyLevel::Maximum {
            return self.select_local_model(query);
        }

        // Rule 2: Domain-specific routing
        if query.domain == Domain::Code {
            return ModelSelection::Local("deepseek-coder:6.7b".into());
        }

        // Rule 3: Complexity-based routing
        match (query.complexity, query.context_size) {
            (Complexity::Simple, _) => {
                ModelSelection::Local("llama3.2:3b".into())
            },
            (Complexity::Complex, size) if size > 16000 => {
                ModelSelection::Local("mistral:7b".into())
            },
            (Complexity::Complex, _) if self.cloud_available() => {
                ModelSelection::Cloud {
                    model: "claude-sonnet-4".into(),
                    sanitize: true,
                }
            },
            _ => ModelSelection::Local("llama3.2:3b".into()),
        }
    }
}
```

**Routing Decision Tree:**
```
Query → Has PII?
    ├─ YES → Local 3B/7B (always)
    └─ NO → Complex?
        ├─ YES → Code query?
        │   ├─ YES → DeepSeek Coder 6.7B
        │   └─ NO → Long context?
        │       ├─ YES → Mistral 7B
        │       └─ NO → Cloud available?
        │           ├─ YES → Claude (sanitized)
        │           └─ NO → Mistral 7B
        └─ NO → Llama 3.2 3B (default)
```

---

## 4. Intelligent Routing Architecture

### 4.1 Privacy-First Query Classification

**Goal:** Automatically classify query sensitivity to route appropriately.

**Three-Tier Classification:**

#### Tier 1: CRITICAL (Always Local)
```
Indicators:
- Contains PII (names, emails, phone, SSN, addresses)
- Medical information (HIPAA)
- Financial data (account numbers, cards)
- Passwords, API keys, credentials
- Private company data

Action: Route to local model in TEE (if available)
Model: Llama 3.2 3B or Mistral 7B (Q4)
Logging: Minimal, encrypted
```

#### Tier 2: SENSITIVE (Prefer Local, Cloud if Sanitized)
```
Indicators:
- Personal opinions, beliefs
- Private communications
- Work-related but non-confidential
- Location data
- Behavioral patterns

Action: Local first, cloud if pseudonymized
Model: Local 3B/7B, or cloud with sanitization
Logging: Aggregated only
```

#### Tier 3: GENERAL (Cloud Allowed)
```
Indicators:
- Public information queries
- General knowledge questions
- News, weather, factual lookups
- Creative writing prompts
- Educational content

Action: Route to cloud for best quality/speed
Model: Claude Sonnet, GPT-4
Logging: Full telemetry allowed
```

### 4.2 PII Detection Implementation

**Approach 1: Local LLM-Based Detection (Recommended)**

```rust
use rust_bert::pipelines::ner::NERModel;

pub struct PIIDetector {
    ner_model: NERModel,
    pattern_matcher: RegexPatternMatcher,
}

impl PIIDetector {
    pub fn detect(&self, text: &str) -> PIIResult {
        // Step 1: NER model (rust-bert)
        let entities = self.ner_model.predict(&[text]);

        // Step 2: Pattern matching for structured PII
        let patterns = self.pattern_matcher.find_all(text);

        // Step 3: Merge and classify
        let pii_items: Vec<PIIItem> = entities.iter()
            .chain(patterns.iter())
            .map(|item| self.classify_sensitivity(item))
            .collect();

        PIIResult {
            has_pii: !pii_items.is_empty(),
            sensitivity: self.calculate_max_sensitivity(&pii_items),
            items: pii_items,
        }
    }
}
```

**Approach 2: Regex Pattern Matching (Fast Fallback)**

```rust
pub struct RegexPatternMatcher {
    patterns: HashMap<PIIType, Regex>,
}

impl RegexPatternMatcher {
    pub fn new() -> Self {
        let mut patterns = HashMap::new();

        // Email
        patterns.insert(
            PIIType::Email,
            Regex::new(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b").unwrap()
        );

        // Phone (US)
        patterns.insert(
            PIIType::Phone,
            Regex::new(r"\b(\+1-)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b").unwrap()
        );

        // SSN
        patterns.insert(
            PIIType::SSN,
            Regex::new(r"\b\d{3}-\d{2}-\d{4}\b").unwrap()
        );

        // Credit Card
        patterns.insert(
            PIIType::CreditCard,
            Regex::new(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b").unwrap()
        );

        Self { patterns }
    }

    pub fn find_all(&self, text: &str) -> Vec<PIIMatch> {
        self.patterns.iter()
            .flat_map(|(pii_type, regex)| {
                regex.find_iter(text).map(|m| PIIMatch {
                    pii_type: *pii_type,
                    start: m.start(),
                    end: m.end(),
                    value: m.as_str().to_string(),
                })
            })
            .collect()
    }
}
```

### 4.3 Pseudonymization Strategy

**Goal:** Preserve context while protecting identity.

**Approach:**
```rust
pub struct Pseudonymizer {
    entity_map: HashMap<String, String>,
    rng: ThreadRng,
}

impl Pseudonymizer {
    pub fn pseudonymize(&mut self, text: &str, pii_items: &[PIIItem]) -> PseudonymizedText {
        let mut result = text.to_string();
        let mut replacements = Vec::new();

        for item in pii_items.iter().rev() {  // Reverse to maintain offsets
            let placeholder = self.generate_placeholder(item);

            // Store mapping for de-pseudonymization
            self.entity_map.insert(placeholder.clone(), item.value.clone());

            // Replace in text
            result.replace_range(item.start..item.end, &placeholder);

            replacements.push(Replacement {
                original: item.value.clone(),
                placeholder: placeholder.clone(),
                pii_type: item.pii_type,
            });
        }

        PseudonymizedText {
            text: result,
            replacements,
        }
    }

    fn generate_placeholder(&mut self, item: &PIIItem) -> String {
        // Use consistent placeholders for same entity type
        match item.pii_type {
            PIIType::PersonName => {
                self.entity_map.get(&item.value).cloned()
                    .unwrap_or_else(|| format!("PERSON_{}", self.rng.gen::<u32>()))
            },
            PIIType::Email => {
                format!("user_{}@example.com", self.rng.gen::<u32>())
            },
            PIIType::Phone => {
                format!("555-0{:03}-{:04}", self.rng.gen_range(100..200), self.rng.gen_range(0..10000))
            },
            PIIType::Location => {
                format!("CITY_{}", self.rng.gen::<u32>())
            },
            _ => format!("[REDACTED_{}]", item.pii_type.as_str()),
        }
    }

    pub fn depseudonymize(&self, text: &str) -> String {
        let mut result = text.to_string();
        for (placeholder, original) in &self.entity_map {
            result = result.replace(placeholder, original);
        }
        result
    }
}
```

### 4.4 Complete Routing Pipeline

**Integrated Architecture:**

```rust
pub struct IntelligentRouter {
    pii_detector: PIIDetector,
    pseudonymizer: Pseudonymizer,
    local_llm: OllamaClient,
    cloud_llm: Option<ClaudeClient>,
    privacy_policy: PrivacyPolicy,
}

impl IntelligentRouter {
    pub async fn process_query(&mut self, query: &str) -> Result<Response> {
        // Step 1: Detect PII
        let pii_result = self.pii_detector.detect(query);

        // Step 2: Classify sensitivity
        let sensitivity = self.classify_query_sensitivity(&pii_result, query);

        // Step 3: Route based on policy
        match (sensitivity, &self.cloud_llm, &self.privacy_policy) {
            // Always local for critical PII
            (SensitivityLevel::Critical, _, _) => {
                self.process_local(query, ModelTier::Small).await
            },

            // Sanitize and route to cloud for general queries
            (SensitivityLevel::General, Some(cloud), _)
                if self.privacy_policy.allow_cloud => {
                self.process_cloud(query).await
            },

            // Pseudonymize for sensitive queries if cloud allowed
            (SensitivityLevel::Sensitive, Some(cloud), _)
                if self.privacy_policy.allow_cloud_sanitized => {
                let sanitized = self.pseudonymizer.pseudonymize(query, &pii_result.items);
                let cloud_response = cloud.query(&sanitized.text).await?;
                let original_response = self.pseudonymizer.depseudonymize(&cloud_response);

                Ok(Response {
                    text: original_response,
                    source: ResponseSource::CloudSanitized,
                    privacy_applied: true,
                })
            },

            // Default: local processing
            _ => {
                self.process_local(query, ModelTier::Small).await
            }
        }
    }

    fn classify_query_sensitivity(&self, pii: &PIIResult, query: &str) -> SensitivityLevel {
        if pii.has_pii && pii.sensitivity >= 0.8 {
            return SensitivityLevel::Critical;
        }

        if pii.has_pii || self.contains_personal_context(query) {
            return SensitivityLevel::Sensitive;
        }

        SensitivityLevel::General
    }
}
```

### 4.5 Production Best Practices

**1. User Control & Transparency:**
```rust
pub struct PrivacyPolicy {
    pub allow_cloud: bool,
    pub allow_cloud_sanitized: bool,
    pub pii_detection_level: PIIDetectionLevel,
    pub show_routing_decisions: bool,  // Explain to user why query routed where
}
```

**2. Privacy Budget Tracking (Differential Privacy):**
```rust
pub struct PrivacyBudgetManager {
    epsilon_budget: f64,
    epsilon_used: f64,
    query_count: usize,
}

impl PrivacyBudgetManager {
    pub fn can_query(&self) -> bool {
        self.epsilon_used < self.epsilon_budget
    }

    pub fn consume_budget(&mut self, query_epsilon: f64) {
        self.epsilon_used += query_epsilon;
        self.query_count += 1;
    }
}
```

**3. Audit Logging:**
```rust
pub struct QueryAuditLog {
    timestamp: DateTime<Utc>,
    query_hash: String,  // SHA-256 of query (not plaintext)
    sensitivity: SensitivityLevel,
    route: RouteDecision,
    pii_detected: bool,
    response_source: ResponseSource,
}
```

---

## 5. RAG Architecture Best Practices

### 5.1 Optimal Chunk Sizes (2024-2025 Research)

**Key Findings from Research:**

**General Recommendations:**
- Common practice: 128-512 tokens
- Factoid queries: 256-512 tokens (best)
- Analytical queries: 1024+ tokens
- Technical documentation: 400-500 tokens

**2024 NVIDIA Benchmark Results:**
```
Tested 7 chunking strategies across 5 datasets:
Winner: Page-level chunking (0.648 accuracy, 0.107 std dev)

Query Type Performance:
- Factoid queries: 256-512 tokens optimal
- Analytical queries: 1024+ tokens optimal
```

**Chroma Research (Recall Comparison):**
```
Performance variance: Up to 9% in recall across methods
- LLMSemanticChunker: 0.919 recall
- ClusterSemanticChunker: 0.913 recall
- RecursiveCharacterTextSplitter: 85.4-89.5% recall
  - Best at 400 tokens: 88.1-89.5%
```

**PKE Recommendation:**

```rust
pub struct ChunkingStrategy {
    pub default_size: usize,      // 400 tokens
    pub overlap: usize,            // 80 tokens (20%)
    pub min_size: usize,           // 128 tokens
    pub max_size: usize,           // 512 tokens
}

impl ChunkingStrategy {
    pub fn chunk_for_document_type(&self, doc_type: DocumentType) -> ChunkConfig {
        match doc_type {
            DocumentType::ShortForm => ChunkConfig {
                size: 256,
                overlap: 50,  // Tweets, notes
            },
            DocumentType::Article => ChunkConfig {
                size: 400,
                overlap: 80,  // Default: articles, blogs
            },
            DocumentType::Technical => ChunkConfig {
                size: 512,
                overlap: 100,  // API docs, technical papers
            },
            DocumentType::Book => ChunkConfig {
                size: 400,
                overlap: 100,  // Long-form content
            },
        }
    }
}
```

**Best Practice: Start with 400-512 tokens + 20% overlap**

### 5.2 Chunking Strategies

**1. RecursiveCharacterTextSplitter (Recommended)**

```rust
pub struct RecursiveTextSplitter {
    chunk_size: usize,
    chunk_overlap: usize,
    separators: Vec<&'static str>,
}

impl RecursiveTextSplitter {
    pub fn new(chunk_size: usize, chunk_overlap: usize) -> Self {
        Self {
            chunk_size,
            chunk_overlap,
            separators: vec!["\n\n", "\n", ". ", " ", ""],
        }
    }

    pub fn split(&self, text: &str) -> Vec<String> {
        self.split_recursive(text, &self.separators)
    }

    fn split_recursive(&self, text: &str, separators: &[&str]) -> Vec<String> {
        if text.len() <= self.chunk_size {
            return vec![text.to_string()];
        }

        if separators.is_empty() {
            return self.force_split(text);
        }

        let separator = separators[0];
        let parts: Vec<&str> = text.split(separator).collect();

        let mut chunks = Vec::new();
        let mut current_chunk = String::new();

        for part in parts {
            if current_chunk.len() + part.len() > self.chunk_size {
                if !current_chunk.is_empty() {
                    chunks.push(current_chunk.clone());
                    // Add overlap
                    let overlap_start = current_chunk.len().saturating_sub(self.chunk_overlap);
                    current_chunk = current_chunk[overlap_start..].to_string();
                }
            }
            current_chunk.push_str(part);
            current_chunk.push_str(separator);
        }

        if !current_chunk.is_empty() {
            chunks.push(current_chunk);
        }

        chunks
    }
}
```

**2. Semantic Chunking (Advanced)**

```rust
pub struct SemanticChunker {
    embedding_model: EmbeddingModel,
    similarity_threshold: f32,
    max_chunk_size: usize,
}

impl SemanticChunker {
    pub async fn chunk(&self, text: &str) -> Result<Vec<SemanticChunk>> {
        // Split into sentences
        let sentences = self.split_sentences(text);

        // Generate embeddings for each sentence
        let embeddings = self.embedding_model.embed_batch(&sentences).await?;

        // Group semantically similar sentences
        let mut chunks = Vec::new();
        let mut current_chunk = vec![sentences[0].to_string()];
        let mut current_embedding = embeddings[0].clone();

        for i in 1..sentences.len() {
            let similarity = cosine_similarity(&current_embedding, &embeddings[i]);

            if similarity > self.similarity_threshold
                && self.chunk_token_count(&current_chunk) < self.max_chunk_size {
                current_chunk.push(sentences[i].to_string());
                current_embedding = self.average_embeddings(&current_embedding, &embeddings[i]);
            } else {
                chunks.push(SemanticChunk {
                    text: current_chunk.join(" "),
                    embedding: current_embedding.clone(),
                });
                current_chunk = vec![sentences[i].to_string()];
                current_embedding = embeddings[i].clone();
            }
        }

        if !current_chunk.is_empty() {
            chunks.push(SemanticChunk {
                text: current_chunk.join(" "),
                embedding: current_embedding,
            });
        }

        Ok(chunks)
    }
}
```

**When to Use Each:**
- **RecursiveCharacterTextSplitter**: Default for most content (fast, reliable)
- **SemanticChunking**: When semantic coherence is critical (academic papers, technical docs)
- **PageLevelChunking**: PDFs with clear page boundaries
- **Hybrid**: Combine methods based on document type

### 5.3 Hybrid Search (BM25 + Semantic)

**Why Hybrid Search?**
- **BM25 (sparse)**: Precise keyword matching, fast
- **Semantic (dense)**: Contextual understanding, handles synonyms
- **Hybrid**: Best of both worlds

**Architecture:**

```rust
pub struct HybridSearchEngine {
    bm25_index: BM25Index,
    vector_store: QdrantClient,
    fusion_algorithm: FusionAlgorithm,
}

impl HybridSearchEngine {
    pub async fn search(&self, query: &str, top_k: usize) -> Result<Vec<SearchResult>> {
        // Step 1: Parallel search
        let (bm25_results, vector_results) = tokio::join!(
            self.bm25_search(query, top_k * 2),
            self.vector_search(query, top_k * 2)
        );

        // Step 2: Fusion (Reciprocal Rank Fusion)
        let fused_results = self.fusion_algorithm.fuse(
            bm25_results?,
            vector_results?,
            top_k
        );

        Ok(fused_results)
    }
}
```

**BM25 Implementation:**

```rust
pub struct BM25Index {
    documents: Vec<Document>,
    inverted_index: HashMap<String, Vec<(usize, usize)>>,  // term -> [(doc_id, freq)]
    avg_doc_length: f32,
    k1: f32,  // 1.2-2.0
    b: f32,   // 0.75
}

impl BM25Index {
    pub fn score(&self, query: &str, doc_id: usize) -> f32 {
        let query_terms = self.tokenize(query);
        let doc_length = self.documents[doc_id].token_count as f32;
        let doc_terms = &self.documents[doc_id].term_frequencies;

        let mut score = 0.0;

        for term in query_terms {
            let df = self.document_frequency(&term);
            let idf = ((self.documents.len() as f32 - df as f32 + 0.5) / (df as f32 + 0.5)).ln();

            if let Some(&tf) = doc_terms.get(&term) {
                let tf = tf as f32;
                let numerator = tf * (self.k1 + 1.0);
                let denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_length / self.avg_doc_length));
                score += idf * (numerator / denominator);
            }
        }

        score
    }
}
```

**Reciprocal Rank Fusion:**

```rust
pub struct ReciprocalRankFusion {
    k: usize,  // Constant, typically 60
}

impl FusionAlgorithm for ReciprocalRankFusion {
    fn fuse(&self,
            bm25_results: Vec<SearchResult>,
            vector_results: Vec<SearchResult>,
            top_k: usize) -> Vec<SearchResult> {

        let mut scores: HashMap<String, f32> = HashMap::new();

        // Score BM25 results
        for (rank, result) in bm25_results.iter().enumerate() {
            let rrf_score = 1.0 / (self.k as f32 + rank as f32 + 1.0);
            *scores.entry(result.id.clone()).or_insert(0.0) += rrf_score;
        }

        // Score vector results
        for (rank, result) in vector_results.iter().enumerate() {
            let rrf_score = 1.0 / (self.k as f32 + rank as f32 + 1.0);
            *scores.entry(result.id.clone()).or_insert(0.0) += rrf_score;
        }

        // Sort by combined score
        let mut combined: Vec<_> = scores.into_iter().collect();
        combined.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());

        // Return top K with original results
        combined.into_iter()
            .take(top_k)
            .map(|(id, score)| self.build_result(id, score, &bm25_results, &vector_results))
            .collect()
    }
}
```

### 5.4 Reranking with Cross-Encoders

**Why Rerank?**
- Bi-encoders (used for initial retrieval): Fast but less accurate
- Cross-encoders: Slower but much more accurate
- Two-stage approach: Best of both

**Performance Impact:**
- Up to 48% improvement in retrieval quality (Databricks)
- +28% NDCG@10 improvement (Pinecone)
- Reduces LLM hallucination rates

**Top Reranking Models (2024-2025):**

| Model | Type | Performance | Speed | License | PKE Fit |
|-------|------|-------------|-------|---------|---------|
| **voyage-rerank-2** | API | ⭐⭐⭐⭐⭐ | Fast | Proprietary | ⚠️ Cloud |
| **Cohere Rerank v3** | API | ⭐⭐⭐⭐⭐ | Fast | Proprietary | ⚠️ Cloud |
| **BGE Reranker Large** | Local | ⭐⭐⭐⭐ | Medium | Apache 2.0 | ✅ Best |
| **cross-encoder/ms-marco-MiniLM-L-6-v2** | Local | ⭐⭐⭐ | Fast | Apache 2.0 | ✅ Good |

**Implementation:**

```rust
use rust_bert::pipelines::sentence_embeddings::CrossEncoderModel;

pub struct Reranker {
    model: CrossEncoderModel,
    top_k: usize,
}

impl Reranker {
    pub fn rerank(&self, query: &str, candidates: Vec<SearchResult>) -> Vec<SearchResult> {
        // Create query-document pairs
        let pairs: Vec<_> = candidates.iter()
            .map(|doc| (query, doc.text.as_str()))
            .collect();

        // Score all pairs with cross-encoder
        let scores = self.model.predict(&pairs).unwrap();

        // Combine scores with original results
        let mut ranked: Vec<_> = candidates.into_iter()
            .zip(scores.into_iter())
            .map(|(mut result, score)| {
                result.rerank_score = Some(score);
                result.final_score = score;  // Override with rerank score
                result
            })
            .collect();

        // Sort by rerank score
        ranked.sort_by(|a, b| b.final_score.partial_cmp(&a.final_score).unwrap());

        // Return top K
        ranked.into_iter().take(self.top_k).collect()
    }
}
```

**Best Practices:**
- Rerank 50-75 documents (sweet spot)
- Use 100-200 for comprehensive web search
- Faster models (MiniLM) for real-time, larger for quality

### 5.5 Complete RAG Pipeline

**Production Architecture:**

```rust
pub struct PKERetrieval {
    chunker: RecursiveTextSplitter,
    embedding_model: OllamaClient,
    hybrid_search: HybridSearchEngine,
    reranker: Reranker,
    context_optimizer: ContextOptimizer,
}

impl PKERetrieval {
    pub async fn retrieve_context(&self, query: &str, max_tokens: usize) -> Result<RetrievalResult> {
        // Step 1: Hybrid search (BM25 + vector)
        let candidates = self.hybrid_search.search(query, 100).await?;

        // Step 2: Rerank with cross-encoder
        let reranked = self.reranker.rerank(query, candidates);

        // Step 3: Optimize context window
        let context = self.context_optimizer.build_context(&reranked, max_tokens);

        Ok(RetrievalResult {
            chunks: context.chunks,
            total_tokens: context.token_count,
            retrieval_quality: context.quality_score,
        })
    }
}
```

**Context Window Optimization:**

```rust
pub struct ContextOptimizer {
    tokenizer: Tokenizer,
}

impl ContextOptimizer {
    pub fn build_context(&self, chunks: &[SearchResult], max_tokens: usize) -> Context {
        let mut context_chunks = Vec::new();
        let mut total_tokens = 0;

        for chunk in chunks {
            let chunk_tokens = self.tokenizer.count_tokens(&chunk.text);

            if total_tokens + chunk_tokens > max_tokens {
                // Try truncation if close to limit
                if chunks.len() == 1 {
                    let truncated = self.tokenizer.truncate(&chunk.text, max_tokens);
                    context_chunks.push(truncated);
                    total_tokens = max_tokens;
                }
                break;
            }

            context_chunks.push(chunk.text.clone());
            total_tokens += chunk_tokens;
        }

        Context {
            chunks: context_chunks,
            token_count: total_tokens,
            quality_score: self.calculate_quality(chunks.len(), total_tokens, max_tokens),
        }
    }

    fn calculate_quality(&self, chunks_used: usize, tokens_used: usize, max_tokens: usize) -> f32 {
        // Higher score if we used diverse chunks without hitting limit
        let diversity_score = (chunks_used as f32 / 10.0).min(1.0);
        let efficiency_score = tokens_used as f32 / max_tokens as f32;

        (diversity_score + efficiency_score) / 2.0
    }
}
```

---

## 6. Hardware-Specific Recommendations

### 6.1 Minimum Viable Setup: 8GB RAM Consumer Hardware

**Target User:** Budget-conscious, basic PKE usage

**Hardware Options:**
```
CPU Path:
- Intel i5-12400 / AMD Ryzen 5 5600 + 8GB DDR4
- MacBook Air M1 (8GB unified memory)
- Cost: $400-800

GPU Path (if available):
- NVIDIA GTX 1660 (6GB) + 8GB system RAM
- Integrated AMD/Intel graphics + 8GB RAM
- Cost: $500-900
```

**Recommended Models:**
```
Primary Model: Llama 3.2 3B Q4_K_M
- Size: ~2GB
- Performance: 150-200 tok/s (CPU), 400-500 tok/s (M1)
- Quality: Comparable to ChatGPT-3.5
- Use case: 90% of queries

Embedding Model: all-MiniLM-L6-v2
- Size: 80MB
- Dimensions: 384
- Speed: ~5000 docs/sec
- Use case: Fast RAG retrieval

Specialized (optional): Phi-3 Mini 3.8B Q4_K_M
- Size: ~2.3GB
- Use case: When 3B isn't sufficient
```

**Vector Database Config:**
```rust
QdrantConfig {
    quantization: ScalarQuantization::Int8,  // 4x memory reduction
    hnsw_config: HnswConfig {
        m: 16,              // Lower connections for memory savings
        ef_construct: 100,
        ef_search: 50,
    },
    max_vectors_in_memory: 50_000,  // ~200MB with quantization
}
```

**Expected Performance:**
- Query latency: 1-3 seconds (first token)
- Generation speed: 150-200 tokens/sec (CPU), 400-500 (M1)
- RAG search: <100ms for 50K documents
- Total memory usage: ~4GB (2GB model + 1GB OS + 1GB vector DB)

**Limitations:**
- Single model loaded at a time
- Context window: 2K-4K tokens (limited by RAM)
- Vector DB: 50K-100K documents max

**PKE Features Supported:**
- ✅ Basic RAG queries
- ✅ PII detection (rust-bert NER)
- ✅ Local-only privacy mode
- ⚠️ Limited context for large documents
- ❌ Multiple simultaneous models

**Verdict:** Perfectly viable for personal knowledge management with lightweight usage.

---

### 6.2 Optimal Setup: 32GB RAM Workstation

**Target User:** Professional/enthusiast, comprehensive PKE usage

**Hardware Options:**
```
CPU Path:
- Intel i7-13700 / AMD Ryzen 7 7700X + 32GB DDR5
- Mac Studio M2 Max (32GB unified memory)
- Mac Mini M4 Pro (32GB unified memory)
- Cost: $1,200-2,000

GPU Path:
- NVIDIA RTX 4060 Ti 16GB + 16GB system RAM = 32GB total
- NVIDIA RTX 3090 24GB + 16GB system RAM = 40GB total (best value)
- Cost: $1,500-2,500
```

**Recommended Model Stack:**
```
Tier 1 - Primary (always loaded):
- Llama 3.2 3B Q4_K_M: ~2GB (fast queries)
- Mistral 7B Q5_K_M: ~5GB (complex queries)
- Total: ~7GB

Tier 2 - Specialized (load on demand):
- DeepSeek Coder 6.7B Q4_K_M: ~4GB (code queries)
- Qwen 2.5 7B Q4_K_M: ~4GB (multilingual)

Embeddings:
- mxbai-embed-large: 330MB (1024 dims)

Total capacity: Can load 2-3 models simultaneously
```

**Vector Database Config:**
```rust
QdrantConfig {
    quantization: ProductQuantization { /* 8-16x reduction */ },
    hnsw_config: HnswConfig {
        m: 32,              // Higher connectivity for quality
        ef_construct: 200,
        ef_search: 100,
    },
    max_vectors_in_memory: 1_000_000,  // ~2GB with PQ
}
```

**Expected Performance:**
- Query latency: 200-500ms (first token)
- Generation speed: 400-800 tokens/sec (depends on CPU/GPU)
- RAG search: <50ms for 1M documents
- Total memory usage: ~15GB (7GB models + 3GB vector DB + 5GB OS/apps)

**Capabilities:**
- ✅ Multiple models loaded simultaneously
- ✅ Intelligent model routing
- ✅ Large context windows (32K-128K tokens)
- ✅ 1M+ document vector database
- ✅ Advanced RAG (hybrid search, reranking)
- ✅ Real-time PII detection and sanitization
- ✅ Simultaneous local + cloud queries

**PKE Features Unlocked:**
- Multi-model routing (code, general, multilingual)
- Full RAG pipeline with reranking
- Large document processing (books, long PDFs)
- Conversation history (thousands of turns)
- Background indexing while querying

**Verdict:** Sweet spot for professional PKE usage - everything works smoothly without compromise.

---

### 6.3 Apple Silicon Optimization Path

**M1/M2/M3/M4 Optimization:**

**Unified Memory Advantage:**
- No separate VRAM - all memory shared between CPU/GPU
- 16GB acts like 24GB in traditional systems (no duplication)
- 32GB acts like 48GB+ (massive advantage)

**M-Series Tiers:**

#### M1/M2 (8GB) - Entry Level
```
Recommended: Llama 3.2 3B Q4_K_M
Performance: 400-600 tok/s
Framework: MLX or Ollama
Memory: ~2-3GB model + 2GB OS + 3GB apps = 7-8GB total
Verdict: Comfortable for single model
```

#### M1/M2 Pro (16GB) - Prosumer
```
Models: Mistral 7B Q4_K_M (primary) + Llama 3.2 3B (fast)
Performance: 250-400 tok/s (Mistral), 500-700 tok/s (Llama)
Framework: MLX (best performance) or Ollama
Memory: 5GB models + 3GB vector DB + 4GB OS = 12GB
Headroom: 4GB for apps
Verdict: Excellent for comprehensive PKE
```

#### M1/M2 Max (32GB) - Professional
```
Models: Mixtral 8x7B Q4_K_M or Qwen 3 30B
Performance: 150-250 tok/s (30B models)
Context: Up to 128K tokens
Framework: MLX with Neural Accelerators
Memory: 15GB models + 5GB vector DB + 8GB OS = 28GB
Capabilities: Near GPT-4 quality locally
Verdict: Top-tier local AI workstation
```

#### M3/M4/M5 Ultra (64GB-192GB) - Extreme
```
Models: 70B-670B parameters possible
Example: DeepSeek AI 670B on M3 Ultra (512GB)
Framework: MLX optimized for M5 Neural Accelerators
Performance: 4x faster TTFT on M5 vs M4 (Neural Accelerators)
Capabilities: Research-grade local inference
Verdict: Cutting-edge, future-proof
```

**MLX-Specific Optimizations:**

```python
# Example MLX configuration for M-series
import mlx.core as mx
import mlx.nn as nn
from mlx_lm import load, generate

# Load model optimized for Apple Silicon
model, tokenizer = load("mistral-7b-v0.1-mlx")

# Configure for M5 Neural Accelerators (if available)
config = {
    "use_neural_accelerators": True,  # M5 only
    "max_tokens": 150,
    "temperature": 0.7,
    "cache_enabled": True,  # Reuse KV cache
}

# Generate with optimized settings
response = generate(model, tokenizer, prompt="Explain Rust", **config)
```

**Performance Comparison (M5 vs M4):**
```
Benchmark Results (Mistral 7B, MLX):
- Time-to-first-token: 4x faster on M5 (Neural Accelerators)
- Token generation: 27% faster on M5 (memory bandwidth)
- Memory bandwidth: 153GB/s (M5) vs 120GB/s (M4) = +28%
- Image generation (FLUX 12B): 3.8x faster on M5

Recommendation: M5 is THE chip for local AI in 2025
```

**Rust Integration on Apple Silicon:**

```rust
// Using candle with Metal backend
use candle::{Device, Tensor};
use candle_transformers::models::llama;

fn main() -> Result<()> {
    // Use Metal backend (optimized for M-series)
    let device = Device::new_metal(0)?;

    // Load model
    let model = llama::Llama::load("models/mistral-7b-mlx", &device)?;

    // Generate
    let tokens = model.generate("Explain quantum computing", 150)?;

    Ok(())
}
```

**PKE Recommendations by M-Series Chip:**

| Chip | RAM | Primary Model | Framework | PKE Capability |
|------|-----|---------------|-----------|----------------|
| **M1/M2** | 8GB | Llama 3.2 3B | Ollama | Basic, single model |
| **M1/M2 Pro** | 16GB | Mistral 7B | MLX or Ollama | Full-featured |
| **M1/M2 Max** | 32GB | Mixtral 8x7B | MLX | Professional |
| **M3/M4 Max** | 64GB | Qwen 3 30B | MLX | Advanced, multi-model |
| **M5 Max** | 64GB | Qwen 3 30B | MLX + Neural Acc. | Best performance |
| **M3/M4 Ultra** | 128GB+ | 70B-670B | MLX | Research-grade |

**Key Takeaway:** Apple Silicon users should prioritize MLX framework for best performance, especially M5 with Neural Accelerators (4x speedup for TTFT).

---

### 6.4 Hardware Decision Matrix

**Quick Selection Guide:**

| Budget | Use Case | Hardware | Models | PKE Capability |
|--------|----------|----------|--------|----------------|
| **<$800** | Casual, basic queries | 8GB RAM system | 1-3B models | ⭐⭐⭐ Good |
| **$800-1500** | Regular use, productivity | 16GB RAM or M2 Pro | 3-7B models | ⭐⭐⭐⭐ Excellent |
| **$1500-2500** | Professional, heavy use | 32GB RAM or M2 Max | 7-30B models | ⭐⭐⭐⭐⭐ Outstanding |
| **$2500+** | Enthusiast, research | RTX 3090 24GB or M3 Ultra | 30-70B models | ⭐⭐⭐⭐⭐ Extreme |

**Platform-Specific Recommendations:**

**Windows/Linux:**
- 8GB: CPU-only, Llama 3.2 3B via Ollama
- 16GB + RTX 4060 Ti 16GB: Best value, Mistral 7B
- 32GB + RTX 3090 24GB: Best price/performance, 30B models
- 48GB + RTX 4090 24GB: High-end, cutting edge

**macOS:**
- M1/M2 8GB: Llama 3.2 3B via MLX
- M2 Pro 16GB: Mistral 7B via MLX (recommended)
- M2 Max 32GB: Mixtral 8x7B via MLX (professional)
- M4/M5 Max 64GB: Qwen 3 30B via MLX + Neural Acc. (best)
- M3 Ultra 128GB+: 70B+ via MLX (extreme)

---

## 7. Production Implementation Roadmap

### Phase 1: MVP (Months 1-3)

**Month 1: Foundation**
- [ ] Integrate Ollama via ollama-rs
- [ ] Implement basic LLM query interface
- [ ] Download and test Llama 3.2 3B, Mistral 7B
- [ ] Build simple prompt templates
- [ ] Basic error handling and retries

**Month 2: RAG Core**
- [ ] Integrate Qdrant (embedded mode)
- [ ] Implement document ingestion pipeline (RecursiveTextSplitter)
- [ ] Generate embeddings with mxbai-embed-large
- [ ] Build retrieval and augmentation logic
- [ ] Test with 10K documents

**Month 3: Privacy & Routing**
- [ ] Implement PII detection (rust-bert NER + regex)
- [ ] Build intelligent model router
- [ ] Add privacy-aware query classification
- [ ] Create user-facing model selection UI
- [ ] Privacy budget tracking (basic)

**Deliverable:** Working PKE with local LLM, RAG, and basic privacy controls.

---

### Phase 2: Advanced RAG (Months 4-6)

**Month 4: Search Enhancements**
- [ ] Implement BM25 index
- [ ] Build hybrid search (BM25 + vector)
- [ ] Add Reciprocal Rank Fusion
- [ ] Advanced metadata filtering
- [ ] Test recall improvement

**Month 5: Reranking & Optimization**
- [ ] Integrate cross-encoder reranker (BGE or ms-marco)
- [ ] Implement semantic chunking (optional)
- [ ] Context window optimization
- [ ] Query performance profiling
- [ ] Optimize chunk sizes per document type

**Month 6: Multi-Modal & Polish**
- [ ] Add code-specific handling (DeepSeek Coder)
- [ ] Multilingual support (Qwen 2.5)
- [ ] Conversation history management
- [ ] Background indexing
- [ ] Performance benchmarking

**Deliverable:** Production-quality RAG with hybrid search, reranking, and optimized performance.

---

### Phase 3: Advanced Features (Months 7-12)

**Month 7-8: Model Ecosystem**
- [ ] Implement dynamic model loading/unloading
- [ ] Multi-model orchestration
- [ ] Model performance monitoring
- [ ] Automatic model updates
- [ ] A/B testing framework

**Month 9-10: Privacy & Security**
- [ ] Secure enclave integration (TEE) for keys
- [ ] Advanced PII detection (LLM-based)
- [ ] Pseudonymization with de-pseudonymization
- [ ] Privacy audit logging
- [ ] Differential privacy for analytics

**Month 11-12: Platform Expansion**
- [ ] Apple Silicon optimization (MLX integration)
- [ ] WASM support for browser UI (candle)
- [ ] Multi-device sync (encrypted)
- [ ] Cloud-local hybrid mode
- [ ] Fine-tuning on personal data (burn)

**Deliverable:** Feature-complete PKE with advanced privacy, multi-platform support, and personalization.

---

### Phase 4: Scale & Intelligence (Months 13+)

- [ ] Self-improving knowledge graph (RuVector GNN layers)
- [ ] Temporal knowledge dynamics (recency weighting)
- [ ] Personal semantic space (fine-tuned embeddings)
- [ ] Multi-modal vector space (text, code, images)
- [ ] Graph-enhanced search (Cypher queries)
- [ ] Agentic RAG with tool use
- [ ] Distributed PKE across devices
- [ ] Custom model quantization optimization

---

## Sources

### Local LLM Runtimes
- [GitHub - vllm-project/vllm](https://github.com/vllm-project/vllm)
- [vLLM 2024 Retrospective and 2025 Vision](https://blog.vllm.ai/2025/01/10/vllm-2024-wrapped-2025-vision.html)
- [Why vLLM is the best choice for AI inference today | Red Hat Developer](https://developers.redhat.com/articles/2025/10/30/why-vllm-best-choice-ai-inference-today)
- [ExLlamaV2: The Fastest Library to Run LLMs | Towards Data Science](https://towardsdatascience.com/exllamav2-the-fastest-library-to-run-llms-32aeda294d26/)
- [A detailed comparison between GPTQ, AWQ, EXL2, q4_K_M, q4_K_S, and load_in_4bit](https://oobabooga.github.io/blog/posts/gptq-awq-exl2-llamacpp/)
- [GitHub - turboderp-org/exllamav2](https://github.com/turboderp-org/exllamav2)
- [Exploring LLMs with MLX and the Neural Accelerators in the M5 GPU - Apple ML Research](https://machinelearning.apple.com/research/exploring-llms-mlx-m5)
- [Apple shows how much faster the M5 runs local LLMs on MLX](https://9to5mac.com/2025/11/20/apple-shows-how-much-faster-the-m5-runs-local-llms-compared-to-the-m4/)
- [Production-Grade Local LLM Inference on Apple Silicon: A Comparative Study](https://arxiv.org/abs/2511.05502)

### Rust-Native Frameworks
- [GitHub - huggingface/candle: Minimalist ML framework for Rust](https://github.com/huggingface/candle)
- [Candle: A New Machine Learning Framework for Rust - The New Stack](https://thenewstack.io/candle-a-new-machine-learning-framework-for-rust/)
- [Using Huggingface with Rust | Shuttle](https://www.shuttle.dev/blog/2024/05/01/using-huggingface-rust)
- [GitHub - tracel-ai/burn](https://github.com/tracel-ai/burn)
- [Burn: The Future of Deep Learning in Rust](https://dev.to/philip_yaw/burn-the-future-of-deep-learning-in-rust-5c5e)
- [Going Big and Small for 2025 | Burn](https://burn.dev/blog/going-big-and-small-for-2025/)
- [GitHub - sonos/tract: Tiny, no-nonsense, self-contained, Tensorflow and ONNX inference](https://github.com/sonos/tract)

### RAG Best Practices
- [What is the optimal chunk size for RAG applications? | Milvus](https://milvus.io/ai-quick-reference/what-is-the-optimal-chunk-size-for-rag-applications)
- [Best Chunking Strategies for RAG in 2025 | Firecrawl](https://www.firecrawl.dev/blog/best-chunking-strategies-rag-2025)
- [Evaluating the Ideal Chunk Size for a RAG System using LlamaIndex](https://www.llamaindex.ai/blog/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5)
- [Chunking for RAG: best practices | Unstructured](https://unstructured.io/blog/chunking-for-rag-best-practices)
- [Optimizing RAG Chunk Size: Your Definitive Guide](https://www.machinelearningplus.com/gen-ai/optimizing-rag-chunk-size-your-definitive-guide-to-better-retrieval-accuracy/)
- [Hybrid Search: Combining BM25 and Semantic Search | LanceDB](https://medium.com/etoai/hybrid-search-combining-bm25-and-semantic-search-for-better-results-with-lan-1358038fe7e6)
- [A Comprehensive Hybrid Search Guide | Elastic](https://www.elastic.co/what-is/hybrid-search)
- [Implementing Hybrid Retrieval (BM25 + FAISS) in RAG](https://www.chitika.com/hybrid-retrieval-rag/)
- [Optimizing RAG with Hybrid Search & Reranking | VectorHub](https://superlinked.com/vectorhub/articles/optimizing-rag-with-hybrid-search-reranking)

### Reranking
- [Top 7 Rerankers for RAG | Analytics Vidhya](https://www.analyticsvidhya.com/blog/2025/06/top-rerankers-for-rag/)
- [The aRt of RAG Part 3: Reranking with Cross Encoders | Medium](https://medium.com/@rossashman/the-art-of-rag-part-3-reranking-with-cross-encoders-688a16b64669)
- [Ultimate Guide to Choosing the Best Reranking Model in 2025](https://www.zeroentropy.dev/articles/ultimate-guide-to-choosing-the-best-reranking-model-in-2025)
- [Rerankers and Two-Stage Retrieval | Pinecone](https://www.pinecone.io/learn/series/rag/rerankers/)
- [Mastering RAG: How to Select A Reranking Model | Galileo](https://galileo.ai/blog/mastering-rag-how-to-select-a-reranking-model)

### Intelligent Routing & Privacy
- [AI Privacy-Minded Router: PII Detection | n8n](https://n8n.io/workflows/5874-ai-privacy-minded-router-pii-detection-for-privacy-security-and-compliance/)
- [PII Detector: hacking privacy in RAG | LlamaIndex](https://www.llamaindex.ai/blog/pii-detector-hacking-privacy-in-rag)
- [PII-Bench: Evaluating Query-Aware Privacy Protection Systems](https://arxiv.org/html/2502.18545v1)
- [Protecting Sensitive and PII information in RAG with Elasticsearch](https://www.elastic.co/search-labs/blog/rag-security-masking-pii)
- [Smarter PII Handling in LLMs: Privacy Without Compromise | Firstsource](https://www.firstsource.com/insights/blogs/when-privacy-meets-performance-smarter-way-handle-pii-llms)

### Hardware Requirements
- [Can You Run This LLM? VRAM Calculator](https://apxml.com/tools/vram-calculator)
- [General recommended VRAM Guidelines for LLMs](https://dev.to/simplr_sh/general-recommended-vram-guidelines-for-llms-4ef3)
- [Run AI Locally: The Best LLMs for 8GB, 16GB, 32GB Memory](https://www.microcenter.com/site/mc-news/article/best-local-llms-8gb-16gb-32gb-memory-guide.aspx)
- [LLM VRAM Usage Compared: Benchmarking 8B–123B Models](https://www.hardware-corner.net/llm-vram-usage-compared/)
- [LLM GPU VRAM Requirements Explained: Complete 2025 Guide](https://www.propelrc.com/llm-gpu-vram-requirements-explained/)

---

## Conclusion

**Key Takeaways:**

1. **Local LLM infrastructure is production-ready** - Multiple mature runtimes (Ollama, llama.cpp, MLX) support offline-first PKE deployment.

2. **Rust ecosystem is robust** - ollama-rs, llama-cpp-rs, candle, burn, tract provide comprehensive Rust-native options.

3. **Privacy can be architecturally guaranteed** - PII detection, intelligent routing, and local-first processing enable true data sovereignty.

4. **RAG best practices are well-established** - 400-512 token chunks, hybrid search (BM25+semantic), cross-encoder reranking deliver state-of-the-art retrieval.

5. **Hardware requirements are accessible** - 8GB minimum viable, 32GB optimal, Apple Silicon path provides best experience.

**Recommended Stack for PKE:**

- **Runtime**: Ollama (primary), MLX (Apple Silicon)
- **Integration**: ollama-rs (critical), rust-bert (NER/embeddings)
- **Models**: Llama 3.2 3B (default), Mistral 7B (complex), mxbai-embed-large (embeddings)
- **Vector DB**: Qdrant (from separate research)
- **Privacy**: rust-bert NER + regex PII detection, intelligent routing
- **RAG**: 400-token chunks, hybrid search, BGE reranker

This architecture achieves PKE's core requirements: data sovereignty, offline-first operation, privacy by design, and excellent performance on consumer hardware.

---

**Document Version:** 1.0
**Last Updated:** December 2025
**Next Review:** March 2026
