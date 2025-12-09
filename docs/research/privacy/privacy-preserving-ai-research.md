# Privacy-Preserving AI Techniques Research

**Research Date:** December 2025
**Focus:** Differential Privacy, Federated Learning, Secure Enclaves, Homomorphic Encryption

## Executive Summary

Privacy-preserving AI has matured significantly in 2024-2025, with production-ready implementations achieving 96.1% accuracy with strong privacy guarantees (ε = 1.9). Multiple approaches exist for PKE implementation, each with distinct trade-offs for data sovereignty and offline-first requirements.

## 1. Differential Privacy (DP)

### Key Findings

**Practical Epsilon Values:**
- ε < 1: Conservative, very strong privacy (recommended for sensitive health data)
- ε = 1-5: Moderate privacy, suitable for data publication
- ε = 5-10: Weak privacy, "better than nothing"
- ε > 10: Not considered meaningful privacy protection
- **Note:** Epsilon is exponential - ε=1 is 8,000x more private than ε=10

**Real-World Deployments:**
- Apple: ε = 14 per day (2017 implementation)
- Healthcare applications: ε = 1.9 achieves 96.1% accuracy
- Recent research shows 5.2% error reduction under strict budgets (ε ≤ 1)

**Key Challenge:** Privacy budget management is cumulative and can only be spent once. Once exhausted, no more queries can be performed on the data.

**PKE Applicability:**
- ✅ **Excellent for:** Query result noise injection, usage analytics, aggregate statistics
- ⚠️ **Challenges:** Privacy budget depletion over time, reduced utility with strong guarantees
- **Recommendation:** Use ε = 0.5-1.0 for PKE query metadata, reserving budget carefully

### Tools & Frameworks

1. **TensorFlow Privacy (TFP)** - Python toolbox for DP-SGD training
2. **OpenMined/PySyft** - Supports both FL and DP techniques
3. **Opacus** (PyTorch) - DP training library

**For PKE:** Consider Rust implementations or Python bindings for local noise injection.

## 2. Federated Learning (FL)

### Technology Landscape

**Core Capability:** Train models collaboratively without sharing raw data - data stays on edge devices.

**2024-2025 Developments:**
- **Hybrid FL-DP:** Combines both techniques for enhanced privacy
- **Edge FL:** 90% of data generated outside data centers by 2025
- **Hierarchical FL:** Multi-layer aggregation with edge-cloud architecture
- **Asynchronous FL:** Blockchain-managed edge devices with consensus groups

**Performance Metrics:**
- Healthcare FL+DP: 96.1% accuracy with ε = 1.9
- Federated adversarial learning: 40% better defense rates with 10% accuracy trade-off
- By 2030: Expected to be standard security layer for distributed AI

### Security Threats

1. **Inference Attacks** - Patterns in aggregated updates leak information
2. **Model Inversion** - Reconstruct training data from model weights
3. **Data Poisoning** - Malicious clients manipulate model updates
4. **Backdoor Attacks** - Hidden triggers in trained models
5. **Eavesdropping** - Unencrypted gradients expose metadata

**PKE Applicability:**
- ⚠️ **Limited for PKE core:** PKE is single-user focused, FL is multi-user collaborative
- ✅ **Potential use:** If PKE develops "knowledge sharing communities" where users opt-in to federated model training
- **Recommendation:** Not priority for MVP, consider for future collaborative features

## 3. Secure Enclaves (TEE)

### Technology Options

#### Intel SGX (Software Guard Extensions)
- **Capability:** Hardware-isolated memory regions ("enclaves") protected from OS/hypervisor
- **Status:** Widely available in Intel Xeon processors
- **Limitation:** Limited enclave memory size (~128-256MB), side-channel vulnerabilities

#### ARM TrustZone
- **Capability:** Hardware-enforced isolation in Cortex-A processors
- **Deployment:** Billions of devices (mobile, embedded)
- **Architecture:** Separate "secure world" and "normal world" execution
- **Limitations:** No support for multiple TEEs, no remote attestation, no memory encryption

#### AMD SEV (Secure Encrypted Virtualization)
- **Capability:** VM-level memory encryption in EPYC processors
- **Advantage:** Entire VM protected, not just enclaves
- **Use Case:** Cloud-based confidential computing

### Development Tools

1. **Open Enclave SDK** - Cross-platform TEE development (Intel SGX, ARM TrustZone)
2. **Mystikos** - Run Linux apps in SGX enclaves
3. **Gramine** (formerly Graphene-SGX) - Library OS for SGX

**PKE Applicability:**
- ✅ **Excellent for:** Protecting LLM API keys, encryption keys, model weights
- ✅ **Use case:** Sensitive classification models (PII detection, routing logic) run in enclave
- ⚠️ **Challenges:** Limited memory, platform dependency, complexity
- **Recommendation:** **HIGH PRIORITY** - Use for cryptographic key storage and sensitive model inference

## 4. Homomorphic Encryption (HE)

### Library Landscape

#### Microsoft SEAL
- **Schemes:** BFV, CKKS
- **License:** MIT
- **Performance:** Best for tasks without bootstrapping
- **Thread Safety:** Generally thread-safe, no native multithreading

#### IBM HElib
- **Schemes:** BGV with bootstrapping, CKKS
- **License:** Apache 2.0
- **Status:** Historical value, wide algorithm selection
- **Limitation:** Multithreading disabled due to thread-safety issues

#### OpenFHE (PALISADE successor)
- **Schemes:** All features of PALISADE + HElib + HEAAN capabilities
- **Status:** Next-generation unified library (2024)
- **Recommendation:** Most comprehensive current option

#### Others
- **Lattigo** (Go) - Multi-party HE by Tune Insight
- **TFHE-rs** (Rust) - Pure Rust implementation by Zama
- **Apple Swift Homomorphic Encryption** - iOS ecosystem integration

### Performance Characteristics

**2024 Benchmarks:**
- **SEAL:** Best single-query performance
- **HEAAN:** Best for homomorphic addition as parameters increase
- **HEonGPU:** Significantly outperforms SEAL with GPU acceleration

**Challenges:**
- Extremely high computational overhead (orders of magnitude slower than plaintext)
- Cannot use for interactive query response times
- Complex parameter tuning

**PKE Applicability:**
- ❌ **Not recommended for PKE:** Too slow for real-time query processing
- ⚠️ **Possible use:** Background processing of encrypted knowledge graphs
- **Recommendation:** **LOW PRIORITY** - Consider only if specific compliance requirement emerges

## 5. Private Information Retrieval (PIR)

### Core Concept

Retrieve items from a database without revealing which item was accessed.

**Relationship to ORAM:**
- **PIR:** Private reads, computationally expensive server-side
- **ORAM:** Private reads/writes, high bandwidth
- **Combined:** Researchers layer PIR over ORAM for optimized bandwidth/computation trade-offs

### 2024 Developments

1. **Piano** (IEEE S&P 2024) - Single-server PIR with sublinear server computation
2. **LightPIR** (ACM Asia CCS 2024) - FHE-based without Gaussian noise
3. **YPIR** (USENIX Security 2024) - Latest advances

**PKE Applicability:**
- ✅ **Interesting for:** Querying cloud-based knowledge repositories without revealing queries
- ⚠️ **Challenges:** Computational overhead, requires server support
- **Recommendation:** **MEDIUM PRIORITY** - Explore for future cloud-sync features with privacy

## Gap Analysis vs PKE Requirements

| Requirement | Best Technology | Feasibility | Priority |
|------------|----------------|-------------|----------|
| Data sovereignty | TEE + Local compute | ✅ High | Critical |
| Offline-first | Local DP noise injection | ✅ High | Critical |
| Query sanitization | NER + PII detection (see other report) | ✅ High | Critical |
| Privacy by architecture | Combination: TEE + DP + local-first | ✅ High | Critical |
| Cloud LLM privacy | DP + Query rewriting | ✅ High | Critical |
| Zero trust | TEE for secrets + encrypted storage | ✅ High | Critical |

## Build vs Integrate Recommendations

### INTEGRATE (High Priority)

1. **Differential Privacy Libraries**
   - Use: TensorFlow Privacy or Opacus via Python bindings
   - Why: Mature, well-tested, good documentation
   - When: MVP phase for query metadata privacy

2. **Secure Enclaves**
   - Use: Open Enclave SDK or Gramine
   - Why: Hardware-backed security for keys and models
   - When: MVP for key storage, Phase 2 for model isolation

3. **PIR Libraries** (Future)
   - Use: Piano or LightPIR
   - Why: Cutting-edge research with production potential
   - When: Post-MVP for cloud sync features

### BUILD (Custom Implementation)

1. **Privacy Coordinator**
   - What: Rust service to manage privacy budgets, route queries
   - Why: PKE-specific privacy policy enforcement
   - When: MVP - critical differentiator

2. **Local DP Noise Injection**
   - What: Lightweight Rust implementation for ε-DP
   - Why: Simple, doesn't require heavy libraries
   - When: MVP for usage analytics

### SKIP (Not Applicable)

1. **Federated Learning** - Not aligned with single-user PKE model
2. **Homomorphic Encryption** - Too slow for interactive queries

## Implementation Roadmap

### Phase 1: MVP (Months 1-3)
- Integrate differential privacy for query metadata (ε = 0.5-1.0)
- Implement TEE for API key storage using Open Enclave SDK
- Build privacy coordinator with budget management

### Phase 2: Enhanced Privacy (Months 4-6)
- Expand TEE usage to sensitive model inference
- Implement query obfuscation pipeline
- Add privacy metrics dashboard

### Phase 3: Advanced Features (Months 7+)
- Explore PIR for cloud knowledge repositories
- Research federated learning for optional community features
- Investigate AMD SEV for full-system protection

## Novel Differentiators for PKE

1. **Adaptive Privacy Budget Management**
   - Automatically adjust ε based on query sensitivity
   - User-configurable privacy vs utility trade-offs
   - Visual privacy dashboard showing budget consumption

2. **Hybrid Local-Cloud Architecture with TEE**
   - Sensitive processing in local TEE enclaves
   - Cloud queries sanitized with mathematically provable privacy
   - Zero-knowledge proof attestations for privacy guarantees

3. **Privacy-First Routing**
   - Automatic sensitivity classification
   - Route sensitive queries to local models in enclaves
   - General queries to cloud with DP noise injection

4. **Transparent Privacy Accounting**
   - Real-time privacy budget tracking
   - Per-query privacy cost estimation
   - Export privacy audit logs

## Sources

1. [Federated learning with differential privacy for breast cancer diagnosis](https://www.nature.com/articles/s41598-025-95858-2)
2. [Privacy-preserving federated learning with intermediate-level model sharing](https://www.sciencedirect.com/science/article/abs/pii/S0957417425021025)
3. [Exploring privacy mechanisms and metrics in federated learning](https://link.springer.com/article/10.1007/s10462-025-11170-5)
4. [Privacy-Preserving AI: Federated Learning Meets Differential Privacy](https://medium.com/@jainultrivedi55555/privacy-preserving-ai-federated-learning-meets-differential-privacy-3ab522485b54)
5. [Trusted execution environment - Wikipedia](https://en.wikipedia.org/wiki/Trusted_execution_environment)
6. [Open Enclave SDK](https://github.com/openenclave/openenclave)
7. [A Comparison of Homomorphic Encryption Libraries HElib, SEAL and FV-NFLlib](https://link.springer.com/chapter/10.1007/978-3-030-12942-2_32)
8. [Fully Homomorphic Encryption Resources](https://fhe.org/resources/)
9. [Prior-itizing Privacy: A Bayesian Approach to Setting the Privacy Budget](https://deep-diver.github.io/neurips2024/posters/kamaxsjxgv/)
10. [Differential Privacy: A Primer](https://www.abhishek-tiwari.com/differential-privacy-a-primer/)
11. [Private Information Retrieval - Wikipedia](https://en.wikipedia.org/wiki/Private_information_retrieval)
12. [Intelligent deep federated learning for IoT edge computing](https://www.nature.com/articles/s41598-025-88163-5)
13. [Federated Learning at the Edge: Enhancing Privacy and Efficiency](https://www.intechopen.com/online-first/1230198)

## Conclusion

Privacy-preserving AI technologies are mature enough for PKE implementation. The recommended approach combines:
- **Secure enclaves (TEE)** for cryptographic operations and sensitive models
- **Differential privacy** for query metadata and analytics
- **Local-first architecture** as foundation for data sovereignty
- **Private Information Retrieval** as future enhancement for cloud features

This combination provides mathematically provable privacy guarantees while maintaining usability.
