# Lightweight Neural Models for Rust Research

**Research Date:** December 2025
**Focus:** Rust ML Libraries, Classification, NER, Embeddings, Routing

## Executive Summary

Rust's machine learning ecosystem has matured significantly in 2024, with production-ready frameworks like rust-bert, Burn, and tch-rs. Multiple options exist for implementing lightweight neural models for PKE's needs: PII detection, query classification, sensitivity routing, and embedding generation. Most models can be kept under 500MB with acceptable accuracy for personal use cases.

## 1. Rust ML Framework Landscape (2024)

### rust-bert - Production NLP Pipelines

**Overview:** Rust native ready-to-use NLP pipelines using transformer models

**Supported Tasks:**
- **Sequence Classification:** Sentiment, topic classification
- **Token Classification:** NER, POS tagging
- **Question Answering:** Extractive QA
- **Text Generation:** GPT-style generation
- **Summarization:** Abstractive and extractive
- **Translation:** Neural machine translation
- **Sentence Embeddings:** Dense vector representations
- **Zero-Shot Classification:** Classification without training data

**Model Support:**
- BERT, DistilBERT, RoBERTa, ALBERT
- GPT-2, GPT-Neo
- BART, T5, Marian
- XLM-RoBERTa (multilingual)

**Performance:**
- Native Rust inference (no Python runtime)
- ONNX model checkpoint support
- CPU and GPU backends
- Multi-threaded inference

**PKE Applicability:**
- ✅ **CRITICAL PRIORITY** - Primary framework for NLP tasks
- ✅ **Use cases:** PII detection (NER), query classification, sentiment analysis
- ✅ **Advantages:** Production-ready, comprehensive, well-maintained

**Example:**
```rust
use rust_bert::pipelines::ner::NERModel;

let ner_model = NERModel::new(Default::default())?;
let input = "My name is John Smith and I live in Seattle";
let output = ner_model.predict(&[input]);

// Output: [(John Smith, PER), (Seattle, LOC)]
```

### Burn Framework

**Overview:** Flexible deep learning framework for Rust (launched 2024)

**Key Features:**
- **Dynamic graphs and shapes** without sacrificing performance
- **Backend agnostic:** CPU, CUDA, Metal, WebGPU, etc.
- **Cross-platform:** Cloud, laptops, mobile, embedded
- **Training and inference** both supported
- **Type-safe:** Leverages Rust's type system
- **Zero-cost abstractions:** No runtime overhead

**Architecture:**
```rust
use burn::{
    nn::{Linear, Relu},
    tensor::Tensor,
};

// Define model
struct Classifier {
    layer1: Linear,
    layer2: Linear,
    relu: Relu,
}

impl Classifier {
    fn forward(&self, x: Tensor) -> Tensor {
        let x = self.layer1.forward(x);
        let x = self.relu.forward(x);
        self.layer2.forward(x)
    }
}
```

**PKE Applicability:**
- ✅ **HIGH PRIORITY** - For custom lightweight models
- ✅ **Use cases:** Query routing, sensitivity classification, small NER models
- ✅ **Advantage:** Full control, can train models specifically for PKE

**Training Considerations:**
- Can train on user's machine with their personal data
- Incremental learning for personalization
- Small model sizes (<100MB) feasible

### tch-rs - PyTorch Bindings for Rust

**Overview:** Rust bindings for PyTorch C++ API

**Features:**
- Full PyTorch functionality in Rust
- GPU acceleration (CUDA, ROCm)
- Automatic differentiation
- Pre-trained model loading
- Dynamic computation graphs

**Advantages:**
- Access to entire PyTorch ecosystem
- Transfer learning from PyTorch models
- Strong GPU support

**Disadvantages:**
- Requires PyTorch installation (C++ libraries)
- Larger dependency footprint

**PKE Applicability:**
- ⚠️ **MEDIUM PRIORITY** - Useful but heavier dependency
- ✅ **Use case:** If need to load PyTorch models directly
- ⚠️ **Consideration:** Conflicts with zero-dependency goal

### Candle - Minimalist ML Framework

**Overview:** Hugging Face's minimalist ML framework for Rust

**Philosophy:**
- Focus on inference, not training
- Minimal dependencies
- Fast compilation
- Good error messages

**Features:**
- CPU, CUDA, Metal backends
- GGML and SafeTensors format support
- Pre-built model examples (LLaMA, Whisper, etc.)

**PKE Applicability:**
- ✅ **INTERESTING** - Lightweight alternative to tch-rs
- ✅ **Use case:** Loading pre-trained models for inference
- ⚠️ **Limitation:** Training support is limited

### Other Notable Libraries

**Linfa:**
- Rust ML framework (sklearn-like API)
- Classical ML: SVM, Random Forest, K-Means, PCA
- Not focused on deep learning
- Good for traditional ML tasks

**Polars + ML:**
- DataFrames + machine learning
- Feature engineering and preprocessing
- Integration with Python ML libs via PyO3

## 2. Model Categories for PKE

### Category 1: PII Detection (NER)

**Requirement:** Identify personally identifiable information in text

**Recommended Approach:** rust-bert with fine-tuned BERT model

**Model Options:**

1. **DistilBERT-based NER (Recommended)**
   - **Size:** ~250MB
   - **Performance:** ~90-95% F1 on PII detection
   - **Latency:** ~50-100ms per document
   - **Training:** Fine-tune on PII datasets (Kaggle, synthetic)

2. **Lightweight LSTM/BiLSTM (Custom)**
   - **Size:** ~10-50MB
   - **Performance:** ~85-90% F1 (slightly lower)
   - **Latency:** ~10-20ms per document
   - **Training:** Train from scratch with Burn

3. **Rule-based + Small Model (Hybrid)**
   - **Size:** ~5-20MB
   - **Performance:** ~88-92% F1
   - **Latency:** ~5-10ms per document
   - **Implementation:** Regex for structured PII + small model for entities

**PKE Recommendation:**
- **MVP:** Hybrid approach (fast, accurate enough)
- **Phase 2:** Add DistilBERT for high-accuracy mode
- **Phase 3:** Train personalized model on user corrections

### Category 2: Query Classification

**Requirement:** Categorize queries by type (question, command, search, etc.)

**Recommended Approach:** Small classifier with Burn or rust-bert

**Model Architecture:**

```rust
// Simple feedforward classifier
Input (query embedding: 384 dims)
  ↓
Hidden Layer 1 (128 neurons, ReLU)
  ↓
Hidden Layer 2 (64 neurons, ReLU)
  ↓
Output (5 classes: question, command, search, create, delete)
```

**Model Size:** ~200KB (weights only)
**Latency:** <5ms
**Accuracy Target:** >90%

**Training Data:**
- Synthetic examples generated by LLM
- User interactions (with permission)
- Public datasets (TREC, DBpedia)

### Category 3: Sensitivity Classification

**Requirement:** Determine if query contains sensitive information

**Recommended Approach:** Binary classifier with Burn

**Model Architecture:**

```rust
Input (query embedding: 384 dims)
  ↓
Dense Layer (256 neurons, ReLU)
  ↓
Dense Layer (128 neurons, ReLU)
  ↓
Dense Layer (64 neurons, ReLU)
  ↓
Output (2 classes: sensitive, not_sensitive)
  ↓
Softmax (probability scores)
```

**Model Size:** ~500KB
**Latency:** <5ms
**Accuracy Target:** >95% (critical for privacy)

**Training Data:**
- Synthetic sensitive queries with PII
- Public/private information examples
- Domain-specific sensitivity (medical, financial, personal)

**Continuous Learning:**
- Update model based on user corrections
- Federated learning across PKE users (optional, privacy-preserving)

### Category 4: Routing Decision Model

**Requirement:** Decide where to route query (local model, cloud LLM)

**Factors to Consider:**
1. Presence of PII (from NER model)
2. Query complexity (from classifier)
3. User privacy settings (paranoid, balanced, minimal)
4. Model availability (which local models loaded)
5. Network availability (offline mode)
6. Resource constraints (battery, CPU)

**Recommended Approach:** Rule-based system with ML confidence scoring

**Architecture:**

```rust
pub struct RoutingDecision {
    destination: Destination, // Local3B, Local7B, Cloud
    confidence: f32,
    reasoning: Vec<String>,
}

pub struct Router {
    pii_detector: NERModel,
    complexity_classifier: ComplexityModel,
    sensitivity_classifier: SensitivityModel,
    user_settings: PrivacySettings,
}

impl Router {
    pub fn route(&self, query: &str) -> RoutingDecision {
        let has_pii = self.pii_detector.predict(query).is_some();
        let complexity = self.complexity_classifier.predict(query);
        let sensitivity = self.sensitivity_classifier.predict(query);

        // Rule-based logic with ML inputs
        if has_pii || sensitivity > 0.8 {
            return RoutingDecision {
                destination: Destination::Local,
                confidence: 1.0,
                reasoning: vec!["Contains PII or sensitive content".to_string()],
            };
        }

        if complexity < 0.3 && self.user_settings.allow_cloud {
            return RoutingDecision {
                destination: Destination::Cloud,
                confidence: 0.9,
                reasoning: vec!["Simple query, no privacy concerns".to_string()],
            };
        }

        // Default to local
        RoutingDecision {
            destination: Destination::Local,
            confidence: 0.7,
            reasoning: vec!["Balanced privacy and utility".to_string()],
        }
    }
}
```

**Complexity:** Rule-based (no ML model needed)
**Latency:** <1ms
**Accuracy:** Dependent on input models

### Category 5: Embedding Models

**Requirement:** Generate vector representations for semantic search

**Recommended Approach:** rust-bert with sentence-transformers

**Model Options:**

1. **all-MiniLM-L6-v2 (Recommended for MVP)**
   - **Size:** ~80MB
   - **Dimensions:** 384
   - **Performance:** Good quality, very fast
   - **Use case:** Default embedding model

2. **all-mpnet-base-v2 (Higher Quality)**
   - **Size:** ~420MB
   - **Dimensions:** 768
   - **Performance:** Better quality, slower
   - **Use case:** High-accuracy mode

3. **multilingual-e5-base (Multilingual)**
   - **Size:** ~560MB
   - **Dimensions:** 768
   - **Languages:** 100+ languages
   - **Use case:** Non-English knowledge bases

**rust-bert Integration:**
```rust
use rust_bert::pipelines::sentence_embeddings::SentenceEmbeddingsModel;

let model = SentenceEmbeddingsModel::new(Default::default())?;
let sentences = ["This is an example sentence", "Each sentence is converted"];
let embeddings = model.encode(&sentences)?;

// embeddings: Vec<Vec<f32>> with shape [batch_size, embedding_dim]
```

**PKE Usage:**
- Embed documents during indexing
- Embed queries for semantic search
- Store embeddings in vector database (Qdrant/RuVector)

## 3. Model Size vs Performance Trade-offs

### Size Categories

**Tiny (<50MB):**
- Simple feedforward networks
- Distilled models
- Limited capacity but very fast
- Good for: Classification, routing

**Small (50-200MB):**
- Small transformers (DistilBERT tiny variants)
- LSTM/BiLSTM models
- Good balance of size and accuracy
- Good for: NER, embeddings (MiniLM)

**Medium (200-500MB):**
- Standard DistilBERT, small BERT variants
- Good accuracy, acceptable size
- Good for: High-accuracy NER, embeddings (mpnet)

**Large (>500MB):**
- Full BERT, RoBERTa, multilingual models
- Best accuracy, significant memory
- Good for: Critical tasks, optional high-quality mode

### PKE Model Budget

**Total Model Footprint Target:** <1GB for all models combined

**Proposed Allocation:**
- **Embedding model:** ~100MB (MiniLM)
- **PII detection:** ~50MB (hybrid approach)
- **Query classifier:** ~1MB (simple feedforward)
- **Sensitivity classifier:** ~1MB (simple feedforward)
- **Spare capacity:** ~350MB for future models or upgrades

**Total:** ~500MB with room to grow

### Quantization for Size Reduction

**Techniques:**

1. **Weight Quantization (FP32 → FP16):**
   - 50% size reduction
   - Minimal accuracy loss (<1%)
   - Easy to implement

2. **Weight Quantization (FP32 → INT8):**
   - 75% size reduction
   - Small accuracy loss (1-3%)
   - Requires calibration

3. **Dynamic Quantization:**
   - Quantize activations at runtime
   - No size reduction but faster inference
   - Complementary to weight quantization

**rust-bert Support:**
- ONNX models can be quantized
- Use ONNX Runtime for quantized inference

**Burn Support:**
- Custom quantization during training
- Post-training quantization utilities

## 4. Training Custom Models for PKE

### When to Train Custom Models

**Train when:**
- Pre-trained models don't fit specific use case
- Need personalization to user's domain/vocabulary
- Want smallest possible model for performance
- Privacy requires training on user's data only

**Use pre-trained when:**
- General-purpose task (classification, NER, embeddings)
- Limited training data
- Faster time to market

### Training Pipeline with Burn

**Example: Sensitivity Classifier**

```rust
use burn::{
    nn::{Linear, Relu, Dropout, loss::CrossEntropyLoss},
    train::{TrainConfig, TrainEpoch},
    optim::AdamConfig,
    tensor::backend::Backend,
};

// 1. Define model
#[derive(Module)]
struct SensitivityClassifier<B: Backend> {
    layer1: Linear<B>,
    layer2: Linear<B>,
    layer3: Linear<B>,
    dropout: Dropout,
}

// 2. Implement forward pass
impl<B: Backend> SensitivityClassifier<B> {
    fn forward(&self, x: Tensor<B, 2>) -> Tensor<B, 2> {
        let x = self.layer1.forward(x);
        let x = Relu::new().forward(x);
        let x = self.dropout.forward(x);

        let x = self.layer2.forward(x);
        let x = Relu::new().forward(x);
        let x = self.dropout.forward(x);

        self.layer3.forward(x)
    }
}

// 3. Training loop
let model = SensitivityClassifier::new(&device);
let optim = AdamConfig::new().init();

for epoch in 0..num_epochs {
    for (inputs, labels) in train_loader {
        let logits = model.forward(inputs);
        let loss = CrossEntropyLoss::new().forward(logits, labels);

        let grads = loss.backward();
        optim.step(model.parameters(), grads);
    }
}
```

### Training Data Generation

**Approach:** Use local LLM (Llama 3.2 3B) to generate synthetic training data

**Example:**
```rust
// Generate synthetic sensitive queries
let prompts = vec![
    "Generate 100 queries containing personal information like names and addresses",
    "Generate 100 queries about medical conditions and health data",
    "Generate 100 queries about financial information and account numbers",
    "Generate 100 general non-sensitive queries about public information",
];

let training_data = generate_synthetic_data(prompts, local_llm);
let labeled_data = label_data(training_data); // 0 = not sensitive, 1 = sensitive
```

**Advantages:**
- No need for external training data (privacy-preserving)
- Can generate domain-specific examples
- Iterative refinement based on user corrections

### Continuous Learning

**Approach:** Update models based on user feedback

**Implementation:**
```rust
pub struct ContinuousLearner {
    model: SensitivityClassifier,
    correction_buffer: Vec<(String, Label)>,
    retrain_threshold: usize,
}

impl ContinuousLearner {
    pub fn record_correction(&mut self, query: String, correct_label: Label) {
        self.correction_buffer.push((query, correct_label));

        if self.correction_buffer.len() >= self.retrain_threshold {
            self.retrain();
        }
    }

    fn retrain(&mut self) {
        // Incremental training on correction buffer
        let batch = prepare_batch(&self.correction_buffer);
        self.model.train_on_batch(batch);
        self.correction_buffer.clear();
    }
}
```

**Benefits:**
- Models adapt to user's specific needs
- Improves accuracy over time
- User-specific customization

## 5. Performance Optimization

### Inference Optimization

**Techniques:**

1. **Model Quantization:** FP32 → FP16 or INT8
2. **Batch Processing:** Process multiple queries together
3. **Model Caching:** Keep models in memory after first use
4. **ONNX Runtime:** Use optimized runtime for rust-bert models
5. **Async Inference:** Don't block main thread

**Example:**
```rust
pub struct ModelCache {
    ner_model: Arc<Mutex<Option<NERModel>>>,
    embedding_model: Arc<Mutex<Option<EmbeddingModel>>>,
}

impl ModelCache {
    pub async fn get_ner_model(&self) -> NERModel {
        let mut cache = self.ner_model.lock().await;
        if cache.is_none() {
            *cache = Some(NERModel::new(Default::default()).unwrap());
        }
        cache.as_ref().unwrap().clone()
    }
}
```

### Batching Strategy

**Challenge:** Balance latency vs throughput

**Approach:**
```rust
pub struct BatchInference {
    batch_size: usize,
    max_wait_ms: u64,
    pending_queries: Vec<Query>,
}

impl BatchInference {
    pub async fn infer(&mut self, query: Query) -> Result {
        self.pending_queries.push(query);

        if self.pending_queries.len() >= self.batch_size {
            return self.process_batch().await;
        }

        // Wait for more queries or timeout
        tokio::time::sleep(Duration::from_millis(self.max_wait_ms)).await;
        self.process_batch().await
    }
}
```

**For PKE:**
- User queries: No batching (immediate response)
- Background indexing: Large batches (e.g., 100 documents)

## 6. Model Deployment Strategy

### Lazy Loading

**Rationale:** Don't load all models on startup (saves memory)

**Implementation:**
```rust
pub enum ModelState {
    Unloaded,
    Loading,
    Loaded(Box<dyn Model>),
}

pub struct LazyModel {
    state: Arc<Mutex<ModelState>>,
    model_path: PathBuf,
}

impl LazyModel {
    pub async fn load(&self) -> &dyn Model {
        let mut state = self.state.lock().await;
        match *state {
            ModelState::Loaded(ref model) => return model.as_ref(),
            ModelState::Loading => {
                // Wait for loading to complete
                drop(state);
                tokio::time::sleep(Duration::from_millis(100)).await;
                return self.load().await;
            }
            ModelState::Unloaded => {
                *state = ModelState::Loading;
                drop(state);

                let model = load_model_from_disk(&self.model_path).await;

                let mut state = self.state.lock().await;
                *state = ModelState::Loaded(Box::new(model));
                // Return model
            }
        }
    }
}
```

### Model Versioning

**Strategy:** Support multiple model versions

**Directory Structure:**
```
~/.pke/models/
  ├── ner/
  │   ├── v1.0.0/
  │   └── v1.1.0/
  ├── embeddings/
  │   ├── minilm-v1/
  │   └── mpnet-v1/
  └── classifiers/
      ├── sensitivity-v1.0.0/
      └── complexity-v1.0.0/
```

**Version Management:**
```rust
pub struct ModelRegistry {
    models: HashMap<String, Vec<ModelVersion>>,
}

impl ModelRegistry {
    pub fn get_latest(&self, model_name: &str) -> Option<&ModelVersion> {
        self.models.get(model_name)?.last()
    }

    pub fn get_version(&self, model_name: &str, version: &str) -> Option<&ModelVersion> {
        self.models.get(model_name)?
            .iter()
            .find(|v| v.version == version)
    }
}
```

## 7. Build vs Integrate Recommendations

### INTEGRATE

1. **rust-bert**
   - **Priority:** CRITICAL
   - **Use for:** NER, embeddings, classification
   - **Models:** DistilBERT for NER, MiniLM for embeddings
   - **Timeline:** Week 1-2 of MVP

2. **Burn Framework**
   - **Priority:** HIGH
   - **Use for:** Custom lightweight models
   - **Models:** Sensitivity classifier, routing classifier
   - **Timeline:** Month 2-3 of MVP

3. **Pre-trained Models**
   - **DistilBERT-NER:** HuggingFace model fine-tuned on PII
   - **all-MiniLM-L6-v2:** Sentence embeddings
   - **Sources:** HuggingFace Hub, ONNX Model Zoo

### BUILD

1. **Query Classifier** (Simple feedforward)
   - **Why:** Specific to PKE's use cases
   - **Size:** ~1MB
   - **Timeline:** Month 2 of MVP

2. **Sensitivity Classifier** (Feedforward)
   - **Why:** Privacy-critical, needs customization
   - **Size:** ~1MB
   - **Timeline:** Month 2 of MVP

3. **Routing Logic** (Rule-based + ML)
   - **Why:** Core differentiator, complex policy
   - **Timeline:** Month 1-2 of MVP

4. **Continuous Learning Pipeline**
   - **Why:** Personalization is key value prop
   - **Timeline:** Month 3-4 of MVP

### SKIP

1. **Training LLMs from scratch** - Use Ollama models
2. **Complex ensemble models** - Too heavyweight for personal use
3. **Cloud-based training** - Conflicts with privacy model

## 8. Implementation Roadmap

### Phase 1: MVP (Months 1-3)

**Month 1: Foundation**
- Integrate rust-bert for embeddings (MiniLM)
- Set up model loading and caching infrastructure
- Build model registry and versioning system

**Month 2: Core Models**
- Integrate DistilBERT-NER for PII detection
- Train simple query classifier with Burn
- Train sensitivity classifier with Burn
- Implement routing logic

**Month 3: Optimization**
- Add model quantization (FP16)
- Implement lazy loading
- Build continuous learning pipeline
- Performance benchmarking and tuning

### Phase 2: Enhanced Intelligence (Months 4-6)

- Train personalized NER on user corrections
- Add multilingual support (e5-multilingual embeddings)
- Implement advanced routing strategies
- Add confidence calibration

### Phase 3: Advanced Features (Months 7+)

- Multi-task learning (single model for multiple tasks)
- Active learning for optimal training data selection
- Federated learning for privacy-preserving model improvements
- On-device model fine-tuning

## 9. Novel Differentiators for PKE

1. **Personalized Intelligence**
   - Models that learn from user's corrections
   - Domain-specific fine-tuning on user's knowledge
   - Adaptive sensitivity based on user's context

2. **Privacy-First Training**
   - All training happens locally using local LLMs
   - No external training data required
   - Synthetic data generation for any domain

3. **Transparent ML**
   - Show user which model made which decision
   - Display confidence scores and reasoning
   - Allow manual overrides that improve models

4. **Lightweight by Design**
   - <1GB total model footprint
   - Fast inference (<100ms)
   - Battery-efficient

5. **Continuous Improvement**
   - Models get better over time automatically
   - No cloud sync required
   - User-specific optimization

## Sources

1. [rust-bert: Rust native NLP pipelines](https://github.com/guillaume-be/rust-bert)
2. [Awesome Rust Machine Learning](https://github.com/vaaaaanquish/Awesome-Rust-MachineLearning)
3. [Best of ML Rust](https://github.com/e-tornike/best-of-ml-rust)
4. [Burn Framework](https://burn.dev/)
5. [Machine Learning in Rust - Lib.rs](https://lib.rs/science/ml)
6. [How to build a Semantic Search Engine in Rust](https://sachaarbonel.medium.com/how-to-build-a-semantic-search-engine-in-rust-e96e6378cfd9)
7. [Neural Networks in Rust](https://www.arewelearningyet.com/neural-networks/)
8. [Rust for Machine Learning and Data Science: The Ultimate Guide 2024](https://www.rapidinnovation.io/post/rust-in-machine-learning-and-data-science-libraries-and-applications)

## Conclusion

Rust's ML ecosystem is ready for PKE implementation:

**Primary Framework: rust-bert**
- Production-ready, comprehensive NLP pipelines
- Perfect for embeddings and NER
- Well-maintained, good documentation

**Custom Models: Burn Framework**
- Flexible, modern, Rust-native
- Ideal for lightweight task-specific models
- Training and inference both supported

**Architecture: Hybrid Approach**
- Use pre-trained models where possible (embeddings, NER base)
- Train custom models for PKE-specific tasks (sensitivity, routing)
- Continuous learning for personalization

**Model Budget: <1GB total**
- Achievable with quantization and smart model selection
- Excellent performance on modern hardware
- Room for future enhancements

This architecture provides PKE with intelligent, privacy-preserving ML capabilities that improve over time.
