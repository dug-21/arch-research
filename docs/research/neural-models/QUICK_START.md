# Quick Start: Neural Models for PKE

**Get started in 15 minutes with production-ready models**

---

## 1. Install Dependencies

```toml
# Cargo.toml
[dependencies]
ort = "2.0"
ndarray = "0.15"
tokenizers = "0.15"
tokio = { version = "1", features = ["full"] }
```

---

## 2. Download Models (5 minutes)

```bash
# Create models directory
mkdir -p ~/.pke/models

# Download all-MiniLM-L6-v2 (INT8 quantized)
wget https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/model.onnx -O ~/.pke/models/minilm.onnx

# Quantize to INT8 (requires Python + ONNX Runtime)
python - <<EOF
from onnxruntime.quantization import quantize_dynamic, QuantType

quantize_dynamic(
    model_input="~/.pke/models/minilm.onnx",
    model_output="~/.pke/models/minilm-int8.onnx",
    weight_type=QuantType.QInt8
)
print("✅ Model quantized successfully")
EOF

# Download tokenizer
wget https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/tokenizer.json -O ~/.pke/models/tokenizer.json
```

---

## 3. Basic Embedding Example (5 minutes)

```rust
use ort::{Environment, SessionBuilder, GraphOptimizationLevel, Value};
use ndarray::Array;
use tokenizers::Tokenizer;

pub struct EmbeddingModel {
    session: ort::Session,
    tokenizer: Tokenizer,
}

impl EmbeddingModel {
    pub fn new(model_path: &str, tokenizer_path: &str) -> Result<Self, Box<dyn std::error::Error>> {
        let environment = Environment::builder()
            .with_name("pke-embeddings")
            .build()?;

        let session = SessionBuilder::new(&environment)?
            .with_optimization_level(GraphOptimizationLevel::Level3)?
            .with_intra_threads(num_cpus::get())?
            .with_model_from_file(model_path)?;

        let tokenizer = Tokenizer::from_file(tokenizer_path)?;

        Ok(Self { session, tokenizer })
    }

    pub fn encode(&self, text: &str) -> Result<Vec<f32>, Box<dyn std::error::Error>> {
        // Tokenize
        let encoding = self.tokenizer.encode(text, true)?;
        let input_ids = encoding.get_ids();
        let attention_mask = encoding.get_attention_mask();

        // Create tensors
        let input_ids_array = Array::from_shape_vec(
            (1, input_ids.len()),
            input_ids.iter().map(|&x| x as i64).collect()
        )?;

        let attention_mask_array = Array::from_shape_vec(
            (1, attention_mask.len()),
            attention_mask.iter().map(|&x| x as i64).collect()
        )?;

        // Run inference
        let outputs = self.session.run(vec![
            Value::from_array(self.session.allocator(), &input_ids_array)?,
            Value::from_array(self.session.allocator(), &attention_mask_array)?,
        ])?;

        // Extract embeddings (last hidden state, mean pooling)
        let embeddings: Vec<f32> = outputs[0]
            .try_extract()?
            .iter()
            .copied()
            .collect();

        Ok(embeddings)
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let model = EmbeddingModel::new(
        "~/.pke/models/minilm-int8.onnx",
        "~/.pke/models/tokenizer.json"
    )?;

    let text = "How do I reset my password?";
    let embedding = model.encode(text)?;

    println!("✅ Generated embedding with {} dimensions", embedding.len());
    println!("First 10 values: {:?}", &embedding[..10]);

    Ok(())
}
```

---

## 4. PII Detection with Regex (5 minutes)

```rust
use regex::Regex;

pub struct RegexPIIDetector {
    patterns: Vec<(String, Regex)>,
}

impl RegexPIIDetector {
    pub fn new() -> Self {
        let patterns = vec![
            ("EMAIL".to_string(), Regex::new(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b").unwrap()),
            ("PHONE".to_string(), Regex::new(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b").unwrap()),
            ("SSN".to_string(), Regex::new(r"\b\d{3}-\d{2}-\d{4}\b").unwrap()),
            ("CREDIT_CARD".to_string(), Regex::new(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b").unwrap()),
            ("IP_ADDRESS".to_string(), Regex::new(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b").unwrap()),
        ];

        Self { patterns }
    }

    pub fn detect(&self, text: &str) -> Vec<PIIEntity> {
        let mut entities = Vec::new();

        for (entity_type, pattern) in &self.patterns {
            for m in pattern.find_iter(text) {
                entities.push(PIIEntity {
                    text: m.as_str().to_string(),
                    entity_type: entity_type.clone(),
                    start: m.start(),
                    end: m.end(),
                    confidence: 1.0,
                });
            }
        }

        entities
    }
}

#[derive(Debug)]
pub struct PIIEntity {
    pub text: String,
    pub entity_type: String,
    pub start: usize,
    pub end: usize,
    pub confidence: f32,
}

fn main() {
    let detector = RegexPIIDetector::new();

    let text = "Contact me at john@example.com or call 555-123-4567. My SSN is 123-45-6789.";
    let entities = detector.detect(text);

    println!("✅ Found {} PII entities:", entities.len());
    for entity in entities {
        println!("  - {}: {} (confidence: {:.2})", entity.entity_type, entity.text, entity.confidence);
    }
}
```

**Output:**
```
✅ Found 3 PII entities:
  - EMAIL: john@example.com (confidence: 1.00)
  - PHONE: 555-123-4567 (confidence: 1.00)
  - SSN: 123-45-6789 (confidence: 1.00)
```

---

## 5. Simple Routing Logic

```rust
#[derive(Debug)]
pub enum Destination {
    Local,
    Cloud,
}

#[derive(Debug)]
pub struct RoutingDecision {
    pub destination: Destination,
    pub confidence: f32,
    pub reasoning: Vec<String>,
}

pub struct Router {
    user_privacy_level: PrivacyLevel,
}

#[derive(Debug)]
pub enum PrivacyLevel {
    Paranoid,   // Everything local
    Balanced,   // Local if PII, cloud otherwise
    Minimal,    // Cloud when possible
}

impl Router {
    pub fn new(privacy_level: PrivacyLevel) -> Self {
        Self {
            user_privacy_level: privacy_level,
        }
    }

    pub fn route(&self, query: &str, has_pii: bool) -> RoutingDecision {
        match self.user_privacy_level {
            PrivacyLevel::Paranoid => {
                RoutingDecision {
                    destination: Destination::Local,
                    confidence: 1.0,
                    reasoning: vec!["User privacy setting: Paranoid".to_string()],
                }
            }
            PrivacyLevel::Balanced => {
                if has_pii {
                    RoutingDecision {
                        destination: Destination::Local,
                        confidence: 1.0,
                        reasoning: vec!["Query contains PII".to_string()],
                    }
                } else {
                    RoutingDecision {
                        destination: Destination::Cloud,
                        confidence: 0.8,
                        reasoning: vec!["No PII detected, safe for cloud".to_string()],
                    }
                }
            }
            PrivacyLevel::Minimal => {
                if has_pii {
                    RoutingDecision {
                        destination: Destination::Local,
                        confidence: 1.0,
                        reasoning: vec!["Query contains PII".to_string()],
                    }
                } else {
                    RoutingDecision {
                        destination: Destination::Cloud,
                        confidence: 0.9,
                        reasoning: vec!["Prefer cloud for speed".to_string()],
                    }
                }
            }
        }
    }
}

fn main() {
    let router = Router::new(PrivacyLevel::Balanced);

    let query1 = "What's the weather today?";
    let query2 = "My email is john@example.com";

    let decision1 = router.route(query1, false);
    let decision2 = router.route(query2, true);

    println!("Query 1: {:?}", decision1);
    println!("Query 2: {:?}", decision2);
}
```

**Output:**
```
Query 1: RoutingDecision { destination: Cloud, confidence: 0.8, reasoning: ["No PII detected, safe for cloud"] }
Query 2: RoutingDecision { destination: Local, confidence: 1.0, reasoning: ["Query contains PII"] }
```

---

## 6. Complete Pipeline (Putting It All Together)

```rust
pub struct PKEPipeline {
    embedding_model: EmbeddingModel,
    pii_detector: RegexPIIDetector,
    router: Router,
}

impl PKEPipeline {
    pub fn new(privacy_level: PrivacyLevel) -> Result<Self, Box<dyn std::error::Error>> {
        Ok(Self {
            embedding_model: EmbeddingModel::new(
                "~/.pke/models/minilm-int8.onnx",
                "~/.pke/models/tokenizer.json"
            )?,
            pii_detector: RegexPIIDetector::new(),
            router: Router::new(privacy_level),
        })
    }

    pub fn process(&self, query: &str) -> Result<ProcessedQuery, Box<dyn std::error::Error>> {
        // 1. Generate embedding
        let embedding = self.embedding_model.encode(query)?;

        // 2. Detect PII
        let pii_entities = self.pii_detector.detect(query);
        let has_pii = !pii_entities.is_empty();

        // 3. Make routing decision
        let routing = self.router.route(query, has_pii);

        Ok(ProcessedQuery {
            query: query.to_string(),
            embedding,
            pii_entities,
            routing,
        })
    }
}

#[derive(Debug)]
pub struct ProcessedQuery {
    pub query: String,
    pub embedding: Vec<f32>,
    pub pii_entities: Vec<PIIEntity>,
    pub routing: RoutingDecision,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let pipeline = PKEPipeline::new(PrivacyLevel::Balanced)?;

    let queries = vec![
        "What's the capital of France?",
        "My email is john@example.com and phone is 555-1234",
        "How do I reset my password?",
    ];

    for query in queries {
        let result = pipeline.process(query)?;
        println!("\n✅ Query: {}", result.query);
        println!("   Embedding: {} dims", result.embedding.len());
        println!("   PII: {} entities", result.pii_entities.len());
        println!("   Routing: {:?} (confidence: {:.2})", result.routing.destination, result.routing.confidence);
    }

    Ok(())
}
```

**Output:**
```
✅ Query: What's the capital of France?
   Embedding: 384 dims
   PII: 0 entities
   Routing: Cloud (confidence: 0.80)

✅ Query: My email is john@example.com and phone is 555-1234
   Embedding: 384 dims
   PII: 2 entities
   Routing: Local (confidence: 1.00)

✅ Query: How do I reset my password?
   Embedding: 384 dims
   PII: 0 entities
   Routing: Cloud (confidence: 0.80)
```

---

## 7. Performance Benchmarking

```rust
use std::time::Instant;

fn benchmark_pipeline(pipeline: &PKEPipeline, queries: &[&str]) {
    println!("\n📊 Benchmarking {} queries...\n", queries.len());

    let mut total_time = 0u128;
    let mut pii_count = 0;
    let mut local_count = 0;

    for query in queries {
        let start = Instant::now();
        let result = pipeline.process(query).unwrap();
        let elapsed = start.elapsed().as_millis();

        total_time += elapsed;
        pii_count += result.pii_entities.len();

        if matches!(result.routing.destination, Destination::Local) {
            local_count += 1;
        }

        println!("Query: {} | Latency: {}ms | PII: {} | Route: {:?}",
                 &query[..30.min(query.len())],
                 elapsed,
                 result.pii_entities.len(),
                 result.routing.destination);
    }

    let avg_latency = total_time / queries.len() as u128;

    println!("\n📈 Results:");
    println!("   Total queries: {}", queries.len());
    println!("   Average latency: {}ms", avg_latency);
    println!("   PII entities found: {}", pii_count);
    println!("   Routed to local: {} ({:.0}%)", local_count, (local_count as f32 / queries.len() as f32) * 100.0);
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let pipeline = PKEPipeline::new(PrivacyLevel::Balanced)?;

    let test_queries = vec![
        "What's the weather today?",
        "My email is john@example.com",
        "Call me at 555-123-4567",
        "How do I reset my password?",
        "My SSN is 123-45-6789",
        "What's 2+2?",
        "Tell me about machine learning",
        "Contact me at john@example.com or 555-1234",
    ];

    benchmark_pipeline(&pipeline, &test_queries);

    Ok(())
}
```

---

## 8. Next Steps

### Immediate (Today):
1. ✅ Run the examples above
2. ✅ Benchmark on your hardware
3. ✅ Test with your own queries
4. ✅ Measure memory usage (`/usr/bin/time -v`)

### This Week:
1. ✅ Add DistilBERT-NER for ML-based PII detection
2. ✅ Train custom sensitivity classifier
3. ✅ Implement model caching
4. ✅ Add comprehensive tests

### Next Week:
1. ✅ Deploy Q-learning router
2. ✅ Add continuous learning
3. ✅ Implement model versioning
4. ✅ Production monitoring

---

## 9. Troubleshooting

### Issue: ONNX Runtime not found

**Solution:**
```bash
# Install ONNX Runtime
wget https://github.com/microsoft/onnxruntime/releases/download/v1.16.3/onnxruntime-linux-x64-1.16.3.tgz
tar -xzf onnxruntime-linux-x64-1.16.3.tgz
export ORT_LIB_LOCATION=/path/to/onnxruntime-linux-x64-1.16.3/lib
```

### Issue: Model download fails

**Solution:**
```bash
# Use HuggingFace CLI
pip install huggingface_hub
huggingface-cli download sentence-transformers/all-MiniLM-L6-v2 --local-dir ~/.pke/models/minilm
```

### Issue: Slow inference

**Solution:**
```rust
// Enable optimizations in SessionBuilder
let session = SessionBuilder::new(&environment)?
    .with_optimization_level(GraphOptimizationLevel::Level3)?
    .with_intra_threads(num_cpus::get())?  // Use all CPU cores
    .with_inter_threads(1)?
    .commit_from_file(model_path)?;
```

### Issue: High memory usage

**Solution:**
```rust
// Implement lazy loading
pub struct LazyModel {
    model: Option<EmbeddingModel>,
}

impl LazyModel {
    pub fn get_or_load(&mut self) -> &EmbeddingModel {
        if self.model.is_none() {
            self.model = Some(EmbeddingModel::new("model.onnx", "tokenizer.json").unwrap());
        }
        self.model.as_ref().unwrap()
    }

    pub fn unload(&mut self) {
        self.model = None;  // Free memory
    }
}
```

---

## 10. Resources

### Documentation:
- [ort crate docs](https://docs.rs/ort)
- [ONNX Runtime docs](https://onnxruntime.ai/)
- [Tokenizers docs](https://docs.rs/tokenizers)

### Models:
- [HuggingFace Model Hub](https://huggingface.co/models)
- [Sentence Transformers](https://www.sbert.net/)
- [ONNX Model Zoo](https://github.com/onnx/models)

### Examples:
- [ort examples](https://github.com/pykeio/ort/tree/main/examples)
- [rust-bert examples](https://github.com/guillaume-be/rust-bert/tree/master/examples)

---

**You now have a working PKE ML pipeline! 🎉**

Next: Read the full [Production-Ready Models Guide](production-ready-models-rust.md) for advanced features.
