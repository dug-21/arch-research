# Query Anonymization & PII Sanitization Research

**Research Date:** December 2025
**Focus:** NER, PII Detection, Text Anonymization, Stylometric Defense

## Executive Summary

PII detection and anonymization technologies have reached production-grade maturity in 2024-2025, with hybrid NLP/ML approaches achieving 94.7% precision and 89.4% recall on real financial documents. Multiple open-source tools exist with specialized Rust implementations possible. Critical for PKE's privacy-by-architecture requirement.

## 1. Named Entity Recognition (NER) for PII

### State of the Art (2024-2025)

**Hybrid Approach (Latest Research):**
- Combines rule-based NLP + ML + custom NER models
- **Performance:** 94.7% precision, 89.4% recall, 91.1% F1-score
- **Real-world validation:** 93% accuracy on actual financial documents
- **Coverage:** Detects names, addresses, phone numbers, emails, IDs, demographic data

**Key Insight:** Hybrid models outperform pure ML approaches by combining:
1. Rule-based patterns for structured data (phone numbers, emails, SSNs)
2. ML models for contextual entities (names, addresses)
3. Custom NER for domain-specific PII (medical records, financial data)

### Production NER Models

#### High-Performance Models (2024)

1. **ab-ai/pii_model** (Fine-tuned BERT)
   - **F1 Score:** ~96% (self-reported)
   - **Coverage:** Dozens of PII categories
   - **Use Case:** Data preprocessing pipelines
   - **Language:** Python/Transformers

2. **Dialogue-Focused NER Models**
   - **Recall:** Near 100% (aggressive detection)
   - **Precision:** Lower (trade-off for comprehensive coverage)
   - **Best for:** Chat/conversation sanitization

3. **Azure AI Language PII Detection**
   - **Method:** NER + pattern matching
   - **Version:** 2024-11-01-preview (enhanced accuracy)
   - **Categories:** Phone, email, addresses, IDs, financial info
   - **Integration:** Cloud API (not suitable for offline PKE)

4. **Evaluation Across Models** (2024 Research)
   - Tested: Mistral 7B, CodeLlama 7B, GraphCodeBERT, CodeT5, CodeBERT
   - Best performer: Korean BERT/ELECTRA (F1 = 0.943)
   - **Note:** High computational requirements for transformer models

### PKE Applicability

✅ **CRITICAL PRIORITY** - Core requirement for query sanitization before cloud LLM routing

**Use Cases:**
1. Pre-process queries before sending to Claude/GPT APIs
2. Redact PII from documents before indexing
3. Sanitize chat history for cloud backup
4. Anonymize exported knowledge graphs

**Challenges:**
- Balancing recall vs precision (false positives reduce utility)
- Language-specific models needed for multilingual support
- Computational overhead of transformer models

## 2. Open-Source Anonymization Tools

### Microsoft Presidio

**Overview:** Open-source data protection and anonymization SDK (Python)

**Architecture:**
- Default: Spacy NER model + custom PII detection logic
- Modular: Pluggable recognizers for different PII types
- Extensible: Add custom entity recognizers

**Predefined Recognizers:**
- Names, email addresses, phone numbers
- Credit card numbers, SSNs, passport numbers
- IP addresses, URLs, dates

**Capabilities:**
1. **Detection:** Identify PII with confidence scores
2. **Anonymization:** Redact, replace, encrypt, hash, mask
3. **De-identification:** Consistent pseudonymization
4. **Structured & Unstructured:** Works on text and structured data

**PKE Integration Path:**
- ✅ Use Presidio as Python service called from Rust
- ✅ Extract recognizer patterns for Rust reimplementation
- ✅ Leverage for initial prototype

### Generative LLM-Based Redaction

**OpenPipe's PII-Redact Models:**
- **Method:** Fine-tuned generative LLM rewrites text with PII removed
- **Output:** Text with "[REDACTED]" or similar tokens
- **Advantage:** Context-aware rewriting (maintains grammatical integrity)
- **Disadvantage:** Slower, requires LLM inference, less deterministic

**PKE Applicability:**
- ⚠️ Interesting approach but conflicts with local-first requirement
- ❌ Cannot rely on cloud LLM for privacy-critical sanitization
- ✅ Could use small local model (Llama 3.2 3B) if acceptable latency

### Other Notable Tools

1. **Private AI (PrivateGPT)**
   - Proprietary de-identification technology
   - Very high accuracy (commercial tool)
   - Not suitable for open-source PKE

2. **Tonic.ai**
   - Enterprise data anonymization platform
   - Combines NER + data synthesis + custom workflows
   - Too heavyweight for PKE

3. **SpaCy NER**
   - Popular NLP library with built-in NER
   - Fast, efficient, extensible
   - Python-based but has Rust alternatives

4. **pii-anonymization (Apache Spark + Stanford CoreNLP)**
   - Open-source, scalable
   - Requires JVM (not ideal for Rust ecosystem)

## 3. Rust-Native NER Solutions

### rust-bert

**Capabilities:**
- Rust bindings for transformer models (BERT, DistilBERT, etc.)
- Supports sequence classification, token classification (NER), question answering
- Zero-shot classification for flexible PII categories
- Can generate sentence embeddings

**Performance:**
- Native Rust inference (no Python runtime)
- Can use ONNX model checkpoints
- Suitable for offline-first deployment

**PKE Applicability:**
- ✅ **HIGH PRIORITY** - Native Rust solution for NER
- ✅ Fine-tune BERT for PII detection with Rust inference
- ✅ Deploy locally for complete data sovereignty

### Implementation Options

1. **Full Transformer (rust-bert)**
   - **Pros:** Best accuracy, pre-trained models available
   - **Cons:** Larger model size (~100-500MB), slower inference
   - **Use case:** High-accuracy PII detection mode

2. **Lightweight Custom Model**
   - **Approach:** Train smaller LSTM/BiLSTM in Rust (Burn framework)
   - **Pros:** Fast, small footprint (<10MB), instant startup
   - **Cons:** Requires training data, potentially lower accuracy
   - **Use case:** Real-time query sanitization

3. **Hybrid Rule-Based + Small Model**
   - **Approach:** Regex patterns for structured PII + small ML model for names/addresses
   - **Pros:** Fast, accurate for common cases, minimal dependencies
   - **Cons:** Less generalizable, requires maintenance
   - **Use case:** MVP implementation

## 4. Stylometric Privacy & Authorship Obfuscation

### Threat Model

**Stylometric Analysis:** Statistical study of linguistic style can identify authors even after basic anonymization.

**Features Analyzed:**
- Vocabulary richness and word frequency distributions
- Sentence length and complexity patterns
- Punctuation habits and syntactic structures
- Function word usage (the, and, but, etc.)
- N-gram patterns and collocations

**Risk for PKE:** If queries are logged by cloud LLMs, stylometric fingerprinting could link queries across sessions or identify users.

### Defense Techniques

#### 1. Manual Obfuscation
- Consciously alter writing style (impractical for automated system)

#### 2. Automated Rewriting
- **Paraphrasing systems:** Rewrite queries while preserving meaning
- **Style transfer models:** Adapt text to generic/neutral style
- **Round-trip translation:** Translate to another language and back

#### 3. Adversarial Techniques
- Train ML models specifically to defeat authorship attribution
- Generate adversarial examples that misclassify authorship

#### 4. Privacy-Preserving NLP
- Apply differential privacy to text generation
- Add calibrated noise to linguistic features

### PKE Applicability

⚠️ **MEDIUM PRIORITY** - Interesting for advanced privacy but adds complexity

**Recommendation:**
- **Phase 1 (MVP):** Focus on PII removal, skip stylometric defense
- **Phase 2:** Add simple paraphrasing for cloud queries
- **Phase 3:** Implement adversarial style obfuscation

**Implementation Approach:**
1. Use small local LLM (Llama 3.2 3B) to paraphrase queries
2. Add prompt: "Rewrite this question in neutral, generic style"
3. Measure utility impact on answer quality

## 5. Query Obfuscation Techniques

### Multi-Query Splitting

**Technique:** Break sensitive queries into multiple innocuous sub-queries

**Example:**
- Original: "What are the tax implications of my $500K crypto sale?"
- Split:
  1. "Explain capital gains tax basics"
  2. "How are digital assets taxed?"
  3. "What are the tax brackets for high income?"

**Advantages:**
- Prevents cloud LLM from seeing full context
- Reduces profiling risk
- Maintains plausible deniability

**Challenges:**
- Requires sophisticated query decomposition
- May reduce answer quality
- Increases number of API calls (cost)

### K-Anonymity for Queries

**Concept:** Ensure each query is indistinguishable from at least K-1 other queries

**Implementation:**
- Generalize specific terms to broader categories
- Add/remove common qualifiers
- Normalize syntax and structure

**Example:**
- "What's the best Italian restaurant in Brooklyn?" → "What's a good restaurant nearby?"

**PKE Applicability:**
- ✅ Useful for reducing profiling
- ⚠️ May reduce answer relevance significantly

### Differential Privacy for Text

**Technique:** Add calibrated noise to query embeddings or token distributions

**Challenges:**
- Difficult to balance privacy and utility in natural language
- May produce nonsensical queries
- Requires careful epsilon tuning

**Status:** Active research area, not production-ready for queries

## Gap Analysis vs PKE Requirements

| Requirement | Technology | Maturity | PKE Fit |
|------------|-----------|----------|---------|
| PII detection | Hybrid NER (rule + ML) | ✅ Production | Perfect |
| Real-time sanitization | rust-bert or lightweight model | ✅ Production | Excellent |
| Offline operation | Local model inference | ✅ Production | Essential |
| Privacy by architecture | Local-only processing | ✅ Conceptual | Core differentiator |
| Stylometric defense | Paraphrasing models | ⚠️ Research | Nice-to-have |
| Query obfuscation | Multi-query splitting | ⚠️ Prototype | Advanced feature |

## Build vs Integrate Recommendations

### INTEGRATE

1. **Microsoft Presidio (Python Service)**
   - **Use for:** Initial prototype and pattern extraction
   - **Timeline:** Weeks 1-4 of MVP
   - **Transition:** Replace with Rust implementation

2. **rust-bert**
   - **Use for:** Production NER inference
   - **Model:** Fine-tuned BERT/DistilBERT for PII
   - **Timeline:** Month 2-3 of MVP

3. **SpaCy Patterns**
   - **Extract:** Rule-based patterns for structured PII
   - **Reimplement:** In Rust with regex
   - **Timeline:** Month 1 of MVP

### BUILD (Custom Rust Implementation)

1. **Query Sanitizer Service**
   - **Components:**
     - Regex-based structured PII detector
     - rust-bert inference for contextual entities
     - Confidence scoring and user override
   - **Priority:** CRITICAL for MVP

2. **Privacy Router**
   - **Logic:** Determine if query is safe for cloud or requires local processing
   - **Factors:** PII detection results, user settings, sensitivity heuristics
   - **Priority:** CRITICAL for MVP

3. **Lightweight NER Model (Future)**
   - **Framework:** Burn or tch-rs
   - **Training:** Custom dataset from Presidio + public PII datasets
   - **Priority:** Phase 2 optimization

### SKIP

1. **Commercial Tools** (Private AI, Tonic.ai) - Cost and closed-source
2. **Cloud-based NER** (Azure AI, AWS Comprehend) - Conflicts with privacy model
3. **Heavy Enterprise Solutions** - Overengineered for single-user PKE

## Implementation Roadmap

### Phase 1: MVP (Months 1-3)

**Month 1:**
- Integrate Presidio for prototyping
- Implement regex-based structured PII detection in Rust
- Build Privacy Router skeleton with basic routing logic

**Month 2:**
- Set up rust-bert with pre-trained NER model
- Fine-tune model on PII detection datasets
- Integrate model inference into sanitization pipeline

**Month 3:**
- Build confidence scoring system
- Implement user feedback loop for false positives/negatives
- Create privacy dashboard showing sanitization stats

### Phase 2: Enhanced Sanitization (Months 4-6)

- Train custom lightweight NER model
- Implement query paraphrasing with local LLM
- Add multi-query splitting for sensitive queries
- Build A/B testing framework for utility vs privacy trade-offs

### Phase 3: Advanced Privacy (Months 7+)

- Implement adversarial stylometric defense
- Research differential privacy for text
- Add k-anonymity transformations
- Develop privacy metrics and user controls

## Novel Differentiators for PKE

1. **Adaptive Sanitization Levels**
   - User-configurable sensitivity (paranoid, balanced, minimal)
   - Per-query privacy level override
   - Visual indicators showing what was redacted

2. **Zero-Knowledge Verification**
   - Prove sanitization occurred without revealing original query
   - Cryptographic commitments to sanitization policy
   - Audit trail for privacy compliance

3. **Semantic-Preserving Anonymization**
   - Maintain query meaning while removing identifiers
   - Replace specifics with appropriate generics
   - Example: "my neighbor John Smith" → "a neighbor" (not "[REDACTED]")

4. **Learning Sanitization Preferences**
   - Train personal model on user corrections
   - Learn which entities user considers sensitive
   - Personalized privacy profiles

5. **Transparent Privacy Impact**
   - Show how sanitization affects answer quality
   - Estimate privacy gain vs utility loss
   - Let user decide trade-off per query

## Sample Implementation (Rust Pseudocode)

```rust
use rust_bert::pipelines::ner::NERModel;
use regex::Regex;

pub struct QuerySanitizer {
    ner_model: NERModel,
    structured_patterns: Vec<Regex>,
    privacy_level: PrivacyLevel,
}

impl QuerySanitizer {
    pub fn sanitize(&self, query: &str) -> SanitizationResult {
        let mut sanitized = query.to_string();
        let mut entities_found = Vec::new();

        // Step 1: Regex-based structured PII
        for pattern in &self.structured_patterns {
            if let Some(captures) = pattern.captures(&sanitized) {
                entities_found.push(Entity {
                    text: captures[0].to_string(),
                    category: pattern.category(),
                    confidence: 1.0,
                });
                sanitized = pattern.replace_all(&sanitized, "[REDACTED]").to_string();
            }
        }

        // Step 2: NER-based contextual entities
        let ner_entities = self.ner_model.predict(&[sanitized.as_str()]);
        for entity in ner_entities {
            if self.is_pii(&entity) && entity.score > 0.85 {
                entities_found.push(entity.clone());
                sanitized = sanitized.replace(&entity.text, "[REDACTED]");
            }
        }

        // Step 3: Determine routing
        let requires_local = !entities_found.is_empty()
            || self.privacy_level == PrivacyLevel::Paranoid;

        SanitizationResult {
            sanitized_query: sanitized,
            entities_removed: entities_found,
            safe_for_cloud: !requires_local,
            confidence: self.calculate_confidence(&entities_found),
        }
    }
}
```

## Evaluation Metrics

1. **Accuracy Metrics:**
   - Precision, Recall, F1-score on PII detection
   - False positive rate (affects user experience)
   - False negative rate (affects privacy)

2. **Performance Metrics:**
   - Latency (target: <100ms for real-time queries)
   - Throughput (queries per second)
   - Memory footprint (model size + runtime)

3. **Privacy Metrics:**
   - PII leak rate (should be 0%)
   - Stylometric defense effectiveness
   - Re-identification resistance

4. **Utility Metrics:**
   - Answer quality degradation
   - User satisfaction with sanitized results
   - Override frequency (indicates false positives)

## Sources

1. [A hybrid rule-based NLP and ML approach for PII detection in financial documents](https://www.nature.com/articles/s41598-025-04971-9)
2. [Comparing Best NER Models For PII Identification](https://www.protecto.ai/blog/best-ner-models-for-pii-identification/)
3. [PBa-LLM: Privacy- and Bias-aware NLP using Named-Entity Recognition](https://arxiv.org/html/2507.02966)
4. [PII anonymization made easy by Microsoft Presidio](https://towardsdatascience.com/building-a-customized-pii-anonymizer-with-microsoft-presidio-b5c2ddfe523b/)
5. [rust-bert: Rust native NLP pipelines](https://github.com/guillaume-be/rust-bert)
6. [Azure AI Language PII Detection](https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/overview)
7. [PII Detection in Low-Resource Languages](https://dl.acm.org/doi/fullHtml/10.1145/3675888.3676036)
8. [I shouldn't be seeing this: anonymize sensitive data while debugging using NLP](https://blog.px.dev/detect-pii/)

## Conclusion

Query anonymization technology is mature and ready for PKE implementation. The recommended architecture:

1. **Hybrid detection:** Regex patterns + rust-bert NER model
2. **Local inference:** Complete data sovereignty with offline operation
3. **Adaptive routing:** Automatic sensitivity detection with user override
4. **Transparent operation:** Show users what was sanitized and why

This provides robust PII protection while maintaining query utility and user trust.
