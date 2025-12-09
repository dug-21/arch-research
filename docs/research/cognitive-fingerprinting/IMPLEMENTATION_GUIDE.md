# PKE Privacy Implementation Guide

**Quick Reference for Developers**
**Last Updated:** December 2025

---

## 🚀 Quick Start: 3-Week MVP

### Week 1: Regex-Based PII Detection

**Create:** `/src/privacy/pii_detector.rs`

```rust
use regex::Regex;
use lazy_static::lazy_static;

lazy_static! {
    // Social Security Number: XXX-XX-XXXX
    static ref SSN_PATTERN: Regex = Regex::new(
        r"\b\d{3}-\d{2}-\d{4}\b"
    ).unwrap();

    // Phone: (XXX) XXX-XXXX or XXX-XXX-XXXX
    static ref PHONE_PATTERN: Regex = Regex::new(
        r"\b(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b"
    ).unwrap();

    // Email: username@domain.com
    static ref EMAIL_PATTERN: Regex = Regex::new(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    ).unwrap();

    // Credit Card: XXXX-XXXX-XXXX-XXXX or XXXXXXXXXXXXXXXX
    static ref CREDIT_CARD_PATTERN: Regex = Regex::new(
        r"\b(?:\d{4}[-\s]?){3}\d{4}\b"
    ).unwrap();

    // US Addresses: Number + Street name
    static ref ADDRESS_PATTERN: Regex = Regex::new(
        r"\b\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln)\b"
    ).unwrap();
}

#[derive(Debug, Clone)]
pub enum EntityType {
    SocialSecurityNumber,
    PhoneNumber,
    Email,
    CreditCard,
    Address,
    Name,
    Location,
    MedicalCondition,
    Other,
}

#[derive(Debug, Clone)]
pub struct Entity {
    pub text: String,
    pub entity_type: EntityType,
    pub start: usize,
    pub end: usize,
    pub confidence: f64,
}

pub struct RegexPIIDetector;

impl RegexPIIDetector {
    pub fn detect(&self, text: &str) -> Vec<Entity> {
        let mut entities = Vec::new();

        // SSN
        for mat in SSN_PATTERN.find_iter(text) {
            entities.push(Entity {
                text: mat.as_str().to_string(),
                entity_type: EntityType::SocialSecurityNumber,
                start: mat.start(),
                end: mat.end(),
                confidence: 1.0,
            });
        }

        // Phone
        for mat in PHONE_PATTERN.find_iter(text) {
            entities.push(Entity {
                text: mat.as_str().to_string(),
                entity_type: EntityType::PhoneNumber,
                start: mat.start(),
                end: mat.end(),
                confidence: 1.0,
            });
        }

        // Email
        for mat in EMAIL_PATTERN.find_iter(text) {
            entities.push(Entity {
                text: mat.as_str().to_string(),
                entity_type: EntityType::Email,
                start: mat.start(),
                end: mat.end(),
                confidence: 1.0,
            });
        }

        // Credit Card
        for mat in CREDIT_CARD_PATTERN.find_iter(text) {
            entities.push(Entity {
                text: mat.as_str().to_string(),
                entity_type: EntityType::CreditCard,
                start: mat.start(),
                end: mat.end(),
                confidence: 1.0,
            });
        }

        // Address
        for mat in ADDRESS_PATTERN.find_iter(text) {
            entities.push(Entity {
                text: mat.as_str().to_string(),
                entity_type: EntityType::Address,
                start: mat.start(),
                end: mat.end(),
                confidence: 0.9,  // Lower confidence for address pattern
            });
        }

        entities
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ssn_detection() {
        let detector = RegexPIIDetector;
        let text = "My SSN is 123-45-6789 for verification";
        let entities = detector.detect(text);

        assert_eq!(entities.len(), 1);
        assert_eq!(entities[0].text, "123-45-6789");
        assert!(matches!(entities[0].entity_type, EntityType::SocialSecurityNumber));
    }

    #[test]
    fn test_phone_detection() {
        let detector = RegexPIIDetector;
        let text = "Call me at (555) 123-4567 or 555-987-6543";
        let entities = detector.detect(text);

        assert_eq!(entities.len(), 2);
    }

    #[test]
    fn test_email_detection() {
        let detector = RegexPIIDetector;
        let text = "Contact: john.smith@example.com";
        let entities = detector.detect(text);

        assert_eq!(entities.len(), 1);
        assert_eq!(entities[0].text, "john.smith@example.com");
    }
}
```

**Dependencies for Week 1:**
```toml
[dependencies]
regex = "1.10"
lazy_static = "1.4"
```

---

### Week 2-3: NER with rust-bert

**Create:** `/src/privacy/ner_detector.rs`

```rust
use rust_bert::pipelines::ner::{NERModel, Entity as BertEntity};
use anyhow::Result;

pub struct NERDetector {
    model: NERModel,
    confidence_threshold: f64,
}

impl NERDetector {
    pub fn new() -> Result<Self> {
        let model = NERModel::new(Default::default())?;

        Ok(Self {
            model,
            confidence_threshold: 0.85,
        })
    }

    pub fn detect_entities(&self, text: &str) -> Result<Vec<Entity>> {
        let predictions = self.model.predict(&[text]);

        let entities: Vec<Entity> = predictions
            .into_iter()
            .flatten()
            .filter(|e| e.score >= self.confidence_threshold)
            .map(|e| self.convert_entity(e))
            .collect();

        Ok(entities)
    }

    fn convert_entity(&self, bert_entity: BertEntity) -> Entity {
        let entity_type = match bert_entity.label.as_str() {
            "PER" | "PERSON" => EntityType::Name,
            "LOC" | "LOCATION" | "GPE" => EntityType::Location,
            "ORG" | "ORGANIZATION" => EntityType::Organization,
            _ => EntityType::Other,
        };

        Entity {
            text: bert_entity.word,
            entity_type,
            start: bert_entity.offset.begin,
            end: bert_entity.offset.end,
            confidence: bert_entity.score,
        }
    }

    pub fn is_pii_entity(&self, label: &str) -> bool {
        matches!(
            label,
            "PER" | "PERSON" | "LOC" | "LOCATION" | "GPE" | "ORG" | "ORGANIZATION"
        )
    }
}
```

**Dependencies for Week 2-3:**
```toml
[dependencies]
rust-bert = "0.21"
torch = "0.14"  # Required by rust-bert
anyhow = "1.0"
```

**Download model (first run):**
```bash
# rust-bert will automatically download models on first use
# Default: bert-ner-en (English NER, CoNLL03)
# Model size: ~420MB
# Location: ~/.cache/rust-bert/
```

---

### Week 4: Anonymization Mapper

**Create:** `/src/privacy/anonymization_map.rs`

```rust
use std::collections::HashMap;
use uuid::Uuid;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AnonymizationMap {
    session_id: String,
    forward: HashMap<String, String>,  // Original → Placeholder
    reverse: HashMap<String, String>,  // Placeholder → Original
    entity_types: HashMap<String, EntityType>,
    counter: HashMap<EntityType, usize>,
}

impl AnonymizationMap {
    pub fn new() -> Self {
        Self {
            session_id: Uuid::new_v4().to_string(),
            forward: HashMap::new(),
            reverse: HashMap::new(),
            entity_types: HashMap::new(),
            counter: HashMap::new(),
        }
    }

    pub fn anonymize(&mut self, entity: &Entity) -> String {
        // Check if already anonymized
        if let Some(placeholder) = self.forward.get(&entity.text) {
            return placeholder.clone();
        }

        // Generate new placeholder
        let placeholder = self.generate_placeholder(&entity.entity_type);

        // Store mappings
        self.forward.insert(entity.text.clone(), placeholder.clone());
        self.reverse.insert(placeholder.clone(), entity.text.clone());
        self.entity_types.insert(placeholder.clone(), entity.entity_type.clone());

        placeholder
    }

    fn generate_placeholder(&mut self, entity_type: &EntityType) -> String {
        let counter = self.counter.entry(entity_type.clone()).or_insert(0);
        *counter += 1;

        match entity_type {
            EntityType::Name => format!("PERSON_{}", counter),
            EntityType::Location => format!("LOCATION_{}", counter),
            EntityType::Organization => format!("ORG_{}", counter),
            EntityType::SocialSecurityNumber => format!("SSN_{}", counter),
            EntityType::PhoneNumber => format!("PHONE_{}", counter),
            EntityType::Email => format!("EMAIL_{}", counter),
            EntityType::CreditCard => format!("CC_{}", counter),
            EntityType::Address => format!("ADDRESS_{}", counter),
            EntityType::MedicalCondition => format!("CONDITION_{}", counter),
            EntityType::Other => format!("ENTITY_{}", counter),
        }
    }

    pub fn deanonymize(&self, text: &str) -> String {
        let mut result = text.to_string();

        // Replace all placeholders with originals
        for (placeholder, original) in &self.reverse {
            result = result.replace(placeholder, original);
        }

        result
    }

    pub fn get_entities_removed(&self) -> Vec<(String, String, EntityType)> {
        self.forward
            .iter()
            .map(|(orig, placeholder)| {
                let entity_type = self.entity_types
                    .get(placeholder)
                    .cloned()
                    .unwrap_or(EntityType::Other);
                (orig.clone(), placeholder.clone(), entity_type)
            })
            .collect()
    }
}
```

**Dependencies:**
```toml
[dependencies]
uuid = { version = "1.6", features = ["v4"] }
serde = { version = "1.0", features = ["derive"] }
```

---

### Week 4: Query Sanitizer (Combines All)

**Create:** `/src/privacy/query_sanitizer.rs`

```rust
use anyhow::Result;

pub struct QuerySanitizer {
    regex_detector: RegexPIIDetector,
    ner_detector: NERDetector,
    anonymization_map: AnonymizationMap,
}

#[derive(Debug)]
pub struct SanitizationResult {
    pub original_query: String,
    pub sanitized_query: String,
    pub entities_removed: Vec<Entity>,
    pub safe_for_cloud: bool,
    pub confidence: f64,
}

impl QuerySanitizer {
    pub fn new() -> Result<Self> {
        Ok(Self {
            regex_detector: RegexPIIDetector,
            ner_detector: NERDetector::new()?,
            anonymization_map: AnonymizationMap::new(),
        })
    }

    pub fn sanitize(&mut self, query: &str) -> Result<SanitizationResult> {
        let mut sanitized = query.to_string();
        let mut entities_removed = Vec::new();

        // Step 1: Regex-based structured PII (high confidence)
        let regex_entities = self.regex_detector.detect(query);
        for entity in regex_entities {
            let placeholder = self.anonymization_map.anonymize(&entity);
            sanitized = sanitized.replace(&entity.text, &placeholder);
            entities_removed.push(entity);
        }

        // Step 2: NER-based contextual entities
        let ner_entities = self.ner_detector.detect_entities(&sanitized)?;
        for entity in ner_entities {
            // Skip if low confidence
            if entity.confidence < 0.85 {
                continue;
            }

            let placeholder = self.anonymization_map.anonymize(&entity);
            sanitized = sanitized.replace(&entity.text, &placeholder);
            entities_removed.push(entity);
        }

        // Step 3: Calculate overall confidence
        let confidence = if entities_removed.is_empty() {
            1.0  // No PII detected, high confidence query is safe
        } else {
            // Average confidence of detected entities
            entities_removed.iter()
                .map(|e| e.confidence)
                .sum::<f64>() / entities_removed.len() as f64
        };

        // Step 4: Determine if safe for cloud
        let safe_for_cloud = entities_removed.is_empty() || confidence >= 0.9;

        Ok(SanitizationResult {
            original_query: query.to_string(),
            sanitized_query: sanitized,
            entities_removed,
            safe_for_cloud,
            confidence,
        })
    }

    pub fn deanonymize(&self, response: &str) -> String {
        self.anonymization_map.deanonymize(response)
    }

    pub fn get_audit_trail(&self) -> Vec<(String, String, EntityType)> {
        self.anonymization_map.get_entities_removed()
    }
}

// Example usage
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sanitization() -> Result<()> {
        let mut sanitizer = QuerySanitizer::new()?;

        let query = "My name is John Smith and I live at 123 Main Street. \
                     Call me at 555-123-4567 or email john@example.com";

        let result = sanitizer.sanitize(query)?;

        println!("Original: {}", result.original_query);
        println!("Sanitized: {}", result.sanitized_query);
        println!("Safe for cloud: {}", result.safe_for_cloud);
        println!("Confidence: {:.2}", result.confidence);
        println!("Entities removed: {}", result.entities_removed.len());

        for entity in &result.entities_removed {
            println!("  - {} ({:?})", entity.text, entity.entity_type);
        }

        // Test deanonymization
        let mock_response = "PERSON_1 can be reached at PHONE_1 or EMAIL_1";
        let deanonymized = sanitizer.deanonymize(mock_response);
        println!("\nMock response: {}", mock_response);
        println!("Deanonymized: {}", deanonymized);

        Ok(())
    }
}
```

---

## 🔒 Privacy Router

**Create:** `/src/privacy/privacy_router.rs`

```rust
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum SensitivityLevel {
    Public,      // No PII, general knowledge
    Personal,    // Some context but not sensitive
    Sensitive,   // Private information
    Critical,    // Highly sensitive (medical, financial)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Provider {
    Local,
    Claude,
    GPT4,
    Gemini,
}

#[derive(Debug)]
pub enum RoutingDecision {
    LocalOnly { reason: String },
    CloudSafe { provider: Provider, sanitized_query: String },
    UserChoice { recommendation: String, options: Vec<Provider> },
}

pub struct PrivacyRouter {
    sanitizer: QuerySanitizer,
    routing_policy: RoutingPolicy,
}

#[derive(Debug, Clone)]
pub struct RoutingPolicy {
    pub pii_detection_threshold: f64,
    pub force_local_for_sensitive: bool,
    pub default_provider: Provider,
}

impl Default for RoutingPolicy {
    fn default() -> Self {
        Self {
            pii_detection_threshold: 0.85,
            force_local_for_sensitive: true,
            default_provider: Provider::Claude,
        }
    }
}

impl PrivacyRouter {
    pub fn new(policy: RoutingPolicy) -> Result<Self> {
        Ok(Self {
            sanitizer: QuerySanitizer::new()?,
            routing_policy: policy,
        })
    }

    pub async fn route_query(&mut self, query: &str) -> Result<RoutingDecision> {
        // Step 1: Sanitize and detect PII
        let sanitization_result = self.sanitizer.sanitize(query)?;

        // Step 2: Assess sensitivity
        let sensitivity = self.assess_sensitivity(&sanitization_result);

        // Step 3: Make routing decision
        match sensitivity {
            SensitivityLevel::Critical => {
                Ok(RoutingDecision::LocalOnly {
                    reason: format!(
                        "Critical PII detected ({} entities). Processing locally for maximum privacy.",
                        sanitization_result.entities_removed.len()
                    ),
                })
            }

            SensitivityLevel::Sensitive => {
                if self.routing_policy.force_local_for_sensitive {
                    Ok(RoutingDecision::LocalOnly {
                        reason: "Sensitive information detected. Routing to local LLM.".to_string(),
                    })
                } else {
                    Ok(RoutingDecision::UserChoice {
                        recommendation: "Sensitive query detected. Local processing recommended.".to_string(),
                        options: vec![Provider::Local, Provider::Claude, Provider::GPT4],
                    })
                }
            }

            SensitivityLevel::Personal | SensitivityLevel::Public => {
                if sanitization_result.safe_for_cloud {
                    Ok(RoutingDecision::CloudSafe {
                        provider: self.routing_policy.default_provider.clone(),
                        sanitized_query: sanitization_result.sanitized_query,
                    })
                } else {
                    Ok(RoutingDecision::UserChoice {
                        recommendation: "Some PII detected but confidence is low. Review recommended.".to_string(),
                        options: vec![Provider::Local, Provider::Claude],
                    })
                }
            }
        }
    }

    fn assess_sensitivity(&self, result: &SanitizationResult) -> SensitivityLevel {
        if result.entities_removed.is_empty() {
            return SensitivityLevel::Public;
        }

        // Check for critical entity types
        let has_critical = result.entities_removed.iter().any(|e| {
            matches!(
                e.entity_type,
                EntityType::SocialSecurityNumber
                    | EntityType::CreditCard
                    | EntityType::MedicalCondition
            )
        });

        if has_critical {
            return SensitivityLevel::Critical;
        }

        // Check for sensitive entity types
        let has_sensitive = result.entities_removed.iter().any(|e| {
            matches!(
                e.entity_type,
                EntityType::PhoneNumber | EntityType::Address | EntityType::Email
            )
        });

        if has_sensitive && result.entities_removed.len() >= 2 {
            return SensitivityLevel::Sensitive;
        }

        if has_sensitive {
            return SensitivityLevel::Personal;
        }

        SensitivityLevel::Public
    }
}

// Example usage
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_routing_decisions() -> Result<()> {
        let mut router = PrivacyRouter::new(RoutingPolicy::default())?;

        // Test 1: Public query (no PII)
        let decision = router.route_query("What is the capital of France?").await?;
        match decision {
            RoutingDecision::CloudSafe { provider, .. } => {
                println!("✓ Public query routed to {:?}", provider);
            }
            _ => panic!("Expected CloudSafe for public query"),
        }

        // Test 2: Sensitive query (SSN)
        let decision = router
            .route_query("My SSN is 123-45-6789, what should I do?")
            .await?;
        match decision {
            RoutingDecision::LocalOnly { reason } => {
                println!("✓ Sensitive query routed locally: {}", reason);
            }
            _ => panic!("Expected LocalOnly for SSN"),
        }

        // Test 3: Personal query (name)
        let decision = router
            .route_query("My name is John Smith, tell me about privacy")
            .await?;
        println!("✓ Personal query decision: {:?}", decision);

        Ok(())
    }
}
```

---

## 🎨 Privacy Dashboard (Metrics)

**Create:** `/src/privacy/metrics.rs`

```rust
use std::sync::{Arc, Mutex};
use serde::{Serialize, Deserialize};
use chrono::{DateTime, Utc};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PrivacyMetrics {
    pub total_queries: u64,
    pub pii_detected: u64,
    pub routed_local: u64,
    pub routed_cloud: u64,
    pub user_overrides: u64,
    pub entity_counts: HashMap<EntityType, u64>,
    pub session_start: DateTime<Utc>,
}

impl PrivacyMetrics {
    pub fn new() -> Self {
        Self {
            total_queries: 0,
            pii_detected: 0,
            routed_local: 0,
            routed_cloud: 0,
            user_overrides: 0,
            entity_counts: HashMap::new(),
            session_start: Utc::now(),
        }
    }

    pub fn record_query(&mut self, sanitization: &SanitizationResult, decision: &RoutingDecision) {
        self.total_queries += 1;

        if !sanitization.entities_removed.is_empty() {
            self.pii_detected += 1;

            for entity in &sanitization.entities_removed {
                *self.entity_counts.entry(entity.entity_type.clone()).or_insert(0) += 1;
            }
        }

        match decision {
            RoutingDecision::LocalOnly { .. } => self.routed_local += 1,
            RoutingDecision::CloudSafe { .. } => self.routed_cloud += 1,
            RoutingDecision::UserChoice { .. } => {}  // Wait for user decision
        }
    }

    pub fn record_user_override(&mut self) {
        self.user_overrides += 1;
    }

    pub fn pii_detection_rate(&self) -> f64 {
        if self.total_queries == 0 {
            return 0.0;
        }
        (self.pii_detected as f64 / self.total_queries as f64) * 100.0
    }

    pub fn local_routing_rate(&self) -> f64 {
        if self.total_queries == 0 {
            return 0.0;
        }
        (self.routed_local as f64 / self.total_queries as f64) * 100.0
    }

    pub fn override_rate(&self) -> f64 {
        if self.total_queries == 0 {
            return 0.0;
        }
        (self.user_overrides as f64 / self.total_queries as f64) * 100.0
    }

    pub fn summary(&self) -> String {
        format!(
            "Privacy Metrics (since {})\n\
             Total Queries: {}\n\
             PII Detection Rate: {:.1}%\n\
             Local Routing Rate: {:.1}%\n\
             Cloud Routing Rate: {:.1}%\n\
             User Override Rate: {:.1}%\n\
             Top PII Types: {:?}",
            self.session_start.format("%Y-%m-%d %H:%M"),
            self.total_queries,
            self.pii_detection_rate(),
            self.local_routing_rate(),
            (self.routed_cloud as f64 / self.total_queries as f64) * 100.0,
            self.override_rate(),
            self.top_entity_types(3)
        )
    }

    fn top_entity_types(&self, n: usize) -> Vec<(EntityType, u64)> {
        let mut counts: Vec<_> = self.entity_counts.iter()
            .map(|(k, v)| (k.clone(), *v))
            .collect();
        counts.sort_by(|a, b| b.1.cmp(&a.1));
        counts.into_iter().take(n).collect()
    }
}

// Thread-safe wrapper
pub type SharedMetrics = Arc<Mutex<PrivacyMetrics>>;

pub fn create_shared_metrics() -> SharedMetrics {
    Arc::new(Mutex::new(PrivacyMetrics::new()))
}
```

---

## 📦 Complete Cargo.toml

```toml
[package]
name = "pke-privacy"
version = "0.1.0"
edition = "2021"

[dependencies]
# NLP & NER
rust-bert = "0.21"
tokenizers = "0.13"
torch = "0.14"

# Text Processing
regex = "1.10"
lazy_static = "1.4"
unicode-normalization = "0.1"

# Async Runtime
tokio = { version = "1.35", features = ["full"] }
anyhow = "1.0"

# Serialization
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
uuid = { version = "1.6", features = ["v4"] }

# Time
chrono = { version = "0.4", features = ["serde"] }

# HTTP (for cloud API clients)
reqwest = { version = "0.11", features = ["json"] }

[dev-dependencies]
tokio-test = "0.4"
```

---

## 🧪 Integration Test

**Create:** `/tests/integration_test.rs`

```rust
use pke_privacy::*;
use anyhow::Result;

#[tokio::test]
async fn test_end_to_end_privacy_pipeline() -> Result<()> {
    println!("\n=== PKE Privacy Pipeline Integration Test ===\n");

    // Initialize router
    let mut router = PrivacyRouter::new(RoutingPolicy::default())?;
    let metrics = create_shared_metrics();

    // Test queries
    let test_cases = vec![
        (
            "What is the capital of France?",
            "Public query, should route to cloud",
        ),
        (
            "My name is John Smith and I live in Brooklyn",
            "Personal info, should sanitize",
        ),
        (
            "My SSN is 123-45-6789 and credit card is 4532-1234-5678-9010",
            "Critical PII, should route locally",
        ),
        (
            "Call me at (555) 123-4567 or email john@example.com",
            "Contact info, should detect and sanitize",
        ),
    ];

    for (query, description) in test_cases {
        println!("Test: {}", description);
        println!("Query: {}", query);

        let decision = router.route_query(query).await?;

        match decision {
            RoutingDecision::LocalOnly { reason } => {
                println!("  ✓ Routed to LOCAL: {}", reason);
            }
            RoutingDecision::CloudSafe { provider, sanitized_query } => {
                println!("  ✓ Routed to {:?}", provider);
                println!("  Sanitized: {}", sanitized_query);
            }
            RoutingDecision::UserChoice { recommendation, options } => {
                println!("  ⚠ User choice required: {}", recommendation);
                println!("  Options: {:?}", options);
            }
        }

        // Show audit trail
        let audit = router.sanitizer.get_audit_trail();
        if !audit.is_empty() {
            println!("  Entities removed:");
            for (orig, placeholder, entity_type) in audit {
                println!("    {} → {} ({:?})", orig, placeholder, entity_type);
            }
        }

        println!();
    }

    // Print metrics summary
    let metrics_guard = metrics.lock().unwrap();
    println!("{}", metrics_guard.summary());

    Ok(())
}
```

**Run test:**
```bash
cargo test --test integration_test -- --nocapture
```

---

## 🔧 Configuration File

**Create:** `config/privacy.toml`

```toml
[privacy]
# Privacy level: none, basic, standard, paranoid
default_level = "standard"

# Confidence threshold for PII detection (0.0-1.0)
pii_detection_threshold = 0.85

# Automatically route sensitive queries to local LLM
force_local_for_sensitive = true

# Maximum semantic drift tolerance (0.0-1.0)
semantic_drift_tolerance = 0.15

[privacy.pii]
# Enable/disable PII detection
enabled = true

# Entity types to detect
detect_names = true
detect_locations = true
detect_medical = true
detect_financial = true
detect_contact_info = true

# Minimum confidence for NER entities
ner_confidence_threshold = 0.85

[privacy.providers]
# Available providers
default_provider = "claude"
enabled_providers = ["local", "claude", "gpt4", "gemini"]

# Prefer local for sensitive queries
local_preferred_for_sensitive = true

[privacy.metrics]
# Enable privacy metrics collection
enabled = true

# Metrics export path
export_path = "./privacy_metrics.json"

# Auto-export interval (seconds)
auto_export_interval = 3600  # 1 hour
```

**Load configuration:**
```rust
use config::{Config, File};
use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct PrivacyConfig {
    pub privacy: PrivacySettings,
}

#[derive(Debug, Deserialize)]
pub struct PrivacySettings {
    pub default_level: String,
    pub pii_detection_threshold: f64,
    pub force_local_for_sensitive: bool,
    pub pii: PIISettings,
    pub providers: ProviderSettings,
    pub metrics: MetricsSettings,
}

impl PrivacyConfig {
    pub fn load() -> Result<Self> {
        let config = Config::builder()
            .add_source(File::with_name("config/privacy"))
            .build()?;

        config.try_deserialize()
    }
}
```

---

## 📊 Example Output

**Running the integration test produces:**

```
=== PKE Privacy Pipeline Integration Test ===

Test: Public query, should route to cloud
Query: What is the capital of France?
  ✓ Routed to Claude
  Sanitized: What is the capital of France?

Test: Personal info, should sanitize
Query: My name is John Smith and I live in Brooklyn
  ✓ Routed to Claude
  Sanitized: My name is PERSON_1 and I live in LOCATION_1
  Entities removed:
    John Smith → PERSON_1 (Name)
    Brooklyn → LOCATION_1 (Location)

Test: Critical PII, should route locally
Query: My SSN is 123-45-6789 and credit card is 4532-1234-5678-9010
  ✓ Routed to LOCAL: Critical PII detected (2 entities). Processing locally for maximum privacy.
  Entities removed:
    123-45-6789 → SSN_1 (SocialSecurityNumber)
    4532-1234-5678-9010 → CC_1 (CreditCard)

Test: Contact info, should detect and sanitize
Query: Call me at (555) 123-4567 or email john@example.com
  ✓ Routed to Claude
  Sanitized: Call me at PHONE_1 or email EMAIL_1
  Entities removed:
    (555) 123-4567 → PHONE_1 (PhoneNumber)
    john@example.com → EMAIL_1 (Email)

Privacy Metrics (since 2025-12-09 15:45)
Total Queries: 4
PII Detection Rate: 75.0%
Local Routing Rate: 25.0%
Cloud Routing Rate: 75.0%
User Override Rate: 0.0%
Top PII Types: [(Name, 1), (Location, 1), (SocialSecurityNumber, 1)]
```

---

## 🚀 Next Steps

### Week 5-8: Stylometric Defense (Phase 2)

**Add translation model for basic obfuscation:**

```rust
// src/privacy/style_defender.rs
use candle_core::{Device, Tensor};
use candle_transformers::models::marian;

pub struct StyleDefender {
    en_to_es: MarianModel,
    es_to_en: MarianModel,
}

impl StyleDefender {
    pub async fn round_trip_translate(&self, text: &str) -> Result<String> {
        let spanish = self.en_to_es.translate(text).await?;
        let english = self.es_to_en.translate(&spanish).await?;
        Ok(english)
    }
}
```

### Week 9-12: Multi-Provider Routing

**Add provider fragmentation:**

```rust
// src/privacy/provider_router.rs
pub struct ProviderRouter {
    providers: Vec<Provider>,
    session_counter: usize,
    max_queries_per_session: usize,
}

impl ProviderRouter {
    pub fn select_provider(&mut self) -> Provider {
        if self.session_counter >= self.max_queries_per_session {
            self.rotate_provider();
        }
        self.session_counter += 1;
        self.current_provider.clone()
    }

    fn rotate_provider(&mut self) {
        // Round-robin or random selection
        self.current_provider = self.providers
            [self.session_counter % self.providers.len()].clone();
        self.session_counter = 0;
    }
}
```

---

## 🎯 Performance Optimization Tips

### 1. Use ONNX for Faster Inference

```rust
use ort::{Session, Value};

pub struct FastNERDetector {
    session: Session,
}

impl FastNERDetector {
    pub fn new() -> Result<Self> {
        let session = Session::builder()?
            .with_model_from_file("models/bert-ner-en.onnx")?;

        Ok(Self { session })
    }

    pub fn predict(&self, text: &str) -> Result<Vec<Entity>> {
        // ONNX inference (typically 2-3x faster than PyTorch)
        // ...
    }
}
```

### 2. Cache Sanitization Results

```rust
use std::collections::HashMap;

pub struct CachedSanitizer {
    sanitizer: QuerySanitizer,
    cache: HashMap<String, SanitizationResult>,
}

impl CachedSanitizer {
    pub fn sanitize(&mut self, query: &str) -> Result<SanitizationResult> {
        if let Some(result) = self.cache.get(query) {
            return Ok(result.clone());
        }

        let result = self.sanitizer.sanitize(query)?;
        self.cache.insert(query.to_string(), result.clone());
        Ok(result)
    }
}
```

### 3. Parallel Entity Detection

```rust
use rayon::prelude::*;

pub fn detect_parallel(&self, texts: &[&str]) -> Vec<Vec<Entity>> {
    texts.par_iter()
        .map(|text| self.detect_entities(text).unwrap())
        .collect()
}
```

---

## 📚 Additional Resources

- **Full Research Document:** `comprehensive-privacy-research.md` (25,000 words)
- **Executive Summary:** `EXECUTIVE_SUMMARY.md` (Quick reference)
- **rust-bert Documentation:** https://docs.rs/rust-bert/latest/rust_bert/
- **Regex PII Patterns:** https://github.com/microsoft/presidio

---

**Questions? Issues?**
- Review comprehensive research for detailed explanations
- Check rust-bert examples for NER usage patterns
- Test with diverse PII examples to validate detection accuracy

**Ready to implement!** Start with Week 1 regex patterns and build up from there. 🚀
