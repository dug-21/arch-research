# Privacy-Preserving AI: Quick Reference for PKE

**Last Updated:** December 2025

## TL;DR - What to Use NOW

### ✅ Implement in MVP (Months 1-3)

| Technique | Rust Library | Use Case | Priority |
|-----------|--------------|----------|----------|
| **Secure Enclaves** | `fortanix/rust-sgx` | API keys, crypto keys, sensitive models | 🔥 CRITICAL |
| **Differential Privacy** | `opendp` | Query metadata, usage analytics | 🔥 CRITICAL |
| **PII Detection** | `rust-bert` | Query sanitization, document processing | 🔥 CRITICAL |

### ⚠️ Consider for Phase 2-3 (Months 4+)

| Technique | Rust Library | Use Case | Priority |
|-----------|--------------|----------|----------|
| **Zero-Knowledge Proofs** | `arkworks` | Privacy verification, audit logs | HIGH |
| **Private Info Retrieval** | `spiral-rs` | Cloud sync, collaborative features | MEDIUM |

### ❌ Skip for PKE

| Technique | Why Skip | Alternative |
|-----------|----------|-------------|
| **Homomorphic Encryption** | 1000-6000x too slow | Use TEE instead |
| **Federated Learning** | Not single-user aligned | Local DP fine-tuning |
| **Garbled Circuits** | Multi-party only | TEE for single-user |

---

## Quick Decision Tree

```
Need to protect...
│
├─ API Keys / Encryption Keys?
│  └─> Use: Fortanix EDP (Secure Enclaves)
│      Performance: 10-30% overhead
│      Status: ✅ Production-ready
│
├─ Query Privacy (from cloud LLMs)?
│  └─> Use: rust-bert (PII) + OpenDP (DP noise)
│      Performance: <1% overhead
│      Status: ✅ Production-ready
│
├─ Usage Analytics?
│  └─> Use: OpenDP (ε=0.5-1.0)
│      Performance: Negligible
│      Status: ✅ Production-ready
│
├─ Prove Privacy (audit logs)?
│  └─> Use: arkworks (zkSNARKs)
│      Performance: 100ms-10s (prove), 10-100ms (verify)
│      Status: ✅ Production-ready
│
├─ Cloud Sync without revealing queries?
│  └─> Use: Spiral PIR
│      Performance: 100-500ms per query
│      Status: ⚠️ Research-grade
│
└─ Interactive queries on encrypted data?
   └─> Don't use HE - too slow!
       Alternative: Process locally or use TEE
```

---

## Library Installation Cheatsheet

### 1. Differential Privacy (OpenDP)

```toml
[dependencies]
opendp = "0.12"
```

```rust
use opendp::measurements::make_laplace;

let epsilon = 1.0;
let sensitivity = 1.0;
let mech = make_laplace(sensitivity, epsilon)?;
let private_result = mech.invoke(&true_count)?;
```

**Documentation:** [docs.opendp.org](https://docs.opendp.org)

### 2. Secure Enclaves (Fortanix EDP)

```toml
[build]
target = "x86_64-fortanix-unknown-sgx"
```

```rust
#[no_mangle]
pub extern "C" fn enclave_main() {
    // Your secure code here
    let secret_key = load_from_secure_storage();
    process_in_enclave(secret_key);
}
```

**Documentation:** [edp.fortanix.com](https://edp.fortanix.com)

### 3. PII Detection (rust-bert)

```toml
[dependencies]
rust-bert = "0.21"
```

```rust
use rust_bert::pipelines::ner::NERModel;

let ner_model = NERModel::new(Default::default())?;
let output = ner_model.predict(&["John Smith works at OpenAI"]);
// Detects: PERSON, ORGANIZATION
```

**Documentation:** [github.com/guillaume-be/rust-bert](https://github.com/guillaume-be/rust-bert)

### 4. Zero-Knowledge Proofs (arkworks)

```toml
[dependencies]
ark-groth16 = "0.4"
ark-bn254 = "0.4"
```

```rust
use ark_groth16::{Groth16, prove, verify};

// Define circuit, generate proof
let proof = prove(&circuit, &witness)?;
let valid = verify(&vk, &public_inputs, &proof)?;
```

**Documentation:** [arkworks.rs](https://arkworks.rs)

### 5. Private Information Retrieval (Spiral)

```toml
[dependencies]
# Check latest from github.com/menonsamir/spiral-rs
```

```rust
// PIR client code
let query = client.generate_query(index);
let response = server.answer_query(&database, &query);
let item = client.recover_item(response);
```

**Repository:** [github.com/menonsamir/spiral-rs](https://github.com/menonsamir/spiral-rs)

---

## Epsilon (ε) Quick Reference

**Differential Privacy Privacy Budget:**

| ε Value | Privacy Level | PKE Use Case |
|---------|---------------|--------------|
| 0.1 | Paranoid | Medical/genetic data |
| 0.5 | Very Strong | Personal diary queries |
| 1.0 | Strong | **General PKE queries** ⭐ |
| 3.0 | Moderate | Aggregated statistics |
| 5.0 | Weak | Usage analytics |
| 10.0 | Minimal | Not meaningful |

**Recommendation:** Use ε=0.5-1.0 for PKE query metadata

**Remember:** Epsilon is exponential - ε=1 is 8,000x more private than ε=10!

---

## Performance Comparison

| Technique | Latency | Throughput | Memory | Battery |
|-----------|---------|------------|--------|---------|
| **Differential Privacy** | < 1% | < 1% | Negligible | ⚡ Low |
| **Secure Enclaves** | 10-30% | 10-30% | +128-256MB | ⚡ Low |
| **PII Detection (NER)** | ~50-200ms | Medium | ~500MB model | ⚡⚡ Medium |
| **Zero-Knowledge Proofs** | 100ms-10s (prove) | Low (prove) | Moderate | ⚡⚡ Medium |
| **PIR** | 100-500ms | Low | Moderate | ⚡⚡⚡ High |
| **Homomorphic Encryption** | ❌ 1000-6000x | ❌ 1000-6000x | High | ❌ Extreme |
| **Federated Learning** | N/A | N/A | Low | ⚡⚡⚡ High |

---

## PKE Privacy Architecture (One Page)

```
┌──────────────────────────────────────────────┐
│              User Queries PKE                │
│  "What did I write about quantum computing?" │
└──────────────────┬───────────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │  PII Detector       │ ← rust-bert
         │  (rust-bert)        │   ~50-200ms
         └─────────┬───────────┘
                   │
         ┌─────────▼─────────────┐
         │  Privacy Router       │
         │  - Has PII? → Local   │
         │  - Safe? → Cloud      │
         └─────────┬─────────────┘
                   │
         ┌─────────┴──────────┐
         ▼                    ▼
┌────────────────┐   ┌────────────────┐
│  Local Path    │   │  Cloud Path    │
├────────────────┤   ├────────────────┤
│ • Query local  │   │ • Add DP noise │ ← OpenDP
│   LLM (Ollama) │   │   (ε=0.5-1.0)  │
│                │   │ • Send to API  │
│ • Model in TEE │   │ • Log with ZKP │ ← arkworks
│   (optional)   │   │                │
└────────────────┘   └────────────────┘
         │                    │
         └─────────┬──────────┘
                   ▼
         ┌─────────────────┐
         │  Privacy Budget │ ← OpenDP
         │  Manager        │
         │  - Track ε used │
         │  - Warn user    │
         └─────────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │  Return Answer  │
         │  + Privacy Info │
         └─────────────────┘
```

**Keys Stored in TEE:** ← Fortanix EDP
- LLM API keys
- Encryption keys
- Master secrets

---

## Common Pitfalls

### ❌ DON'T

1. **Don't implement crypto primitives yourself**
   - Use audited libraries (OpenDP, TFHE-rs, arkworks)
   - Crypto is extremely hard to get right

2. **Don't use HE for interactive queries**
   - 1000-6000x too slow
   - Use TEE or process locally instead

3. **Don't assume DP alone protects individual queries**
   - DP protects aggregates, not single queries
   - Combine with PII detection for query-level protection

4. **Don't forget privacy budget tracking**
   - DP budget depletes over time
   - Must track cumulative epsilon usage

5. **Don't trust without verification**
   - Add ZKP proofs for critical privacy claims
   - Transparency builds user trust

### ✅ DO

1. **Use layered defenses**
   - Hardware (TEE) + Software (DP) + Protocol (ZKP)
   - Multiple independent protections

2. **Make privacy visible**
   - Show users what was sanitized
   - Display privacy budget consumption
   - Explain routing decisions

3. **Test with real PII**
   - Use realistic test data
   - Measure false positive/negative rates
   - Tune detection thresholds carefully

4. **Plan for failure**
   - What if TEE is compromised?
   - What if PII detection misses something?
   - Defense in depth

5. **Stay updated**
   - New vulnerabilities discovered regularly (Spectre, etc.)
   - Monitor security advisories
   - Update libraries frequently

---

## When to Reassess

**Revisit this analysis if:**

1. ✅ New Rust privacy library reaches 1.0 (e.g., mature FL framework)
2. ✅ Performance breakthrough in HE (>100x speedup)
3. ✅ TEE vulnerability discovered (Spectre-class)
4. ✅ PKE adds collaborative features (triggers FL, MPC use cases)
5. ✅ Regulatory requirements change (GDPR updates, etc.)
6. ✅ 6 months pass (check for new research)

**Next review:** March 2026

---

## Quick Links

### Documentation
- OpenDP: [docs.opendp.org](https://docs.opendp.org)
- Fortanix EDP: [edp.fortanix.com/docs](https://edp.fortanix.com/docs)
- rust-bert: [github.com/guillaume-be/rust-bert](https://github.com/guillaume-be/rust-bert)
- arkworks: [arkworks.rs](https://arkworks.rs)
- TFHE-rs: [docs.zama.ai/tfhe-rs](https://docs.zama.ai/tfhe-rs)

### Research
- PPAI Workshop: [ppai-workshop.github.io](https://ppai-workshop.github.io)
- FHE.org: [fhe.org/resources](https://fhe.org/resources)
- ZKP Science: [zkp.science](https://zkp.science)

### Tools
- Awesome Rust Crypto: [cryptography.rs](https://cryptography.rs)
- OpenDP Community: [opendp.org](https://opendp.org)

---

**For comprehensive analysis, see:** `rust-privacy-techniques-comprehensive.md`
