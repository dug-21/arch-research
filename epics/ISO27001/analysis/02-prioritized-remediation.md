# ISO 27001 Prioritized Remediation Plan

**Organization:** Small B2B Non-Profit Services Provider
**Assessment Date:** November 4, 2025
**Certification Target:** 12-18 months from project start

---

## Priority Classification System

| Priority | Criteria | Timeline | Risk Level |
|----------|----------|----------|------------|
| **P0 - Critical** | Audit-blocking, cannot certify without | Month 1-8 | Critical |
| **P1 - High** | High risk, required for certification | Month 4-10 | High |
| **P2 - Medium** | Required but partial implementation acceptable | Month 6-12 | Medium |
| **P3 - Low** | Can be deferred to post-certification | Month 12+ | Low |

---

## P0 - Critical Priority Controls (28 Controls)

### Must Complete for Certification Audit

| Control | Description | Effort (Weeks) | Cost | Dependencies | Quick Win? |
|---------|-------------|----------------|------|--------------|------------|
| **A.5.1** | Information security policy | 4-6 | $5K-10K | Executive approval | ⚡ Yes (templates) |
| **A.5.2** | Policy review process | 1-2 | $1K-2K | A.5.1 complete | ⚡ Yes |
| **A.5.3** | Topic-specific policies | 6-8 | $10K-20K | A.5.1 complete | No |
| **A.8.1** | Asset inventory | 6-8 | $5K-10K | Tool selection | No |
| **A.8.5** | Data classification | 4-6 | $3K-5K | Asset inventory | No |
| **A.9.1** | Access control policy | 3-4 | $3K-5K | A.5.1 complete | No |
| **A.9.2** | User access provisioning | 4-6 | $5K-10K | A.9.1 complete | ⚡ Yes (cloud IAM) |
| **A.9.3** | Privileged access mgmt | 4-6 | $10K-20K | A.9.1 complete | No |
| **A.9.5** | User access reviews | 2-3 | $2K-5K | A.9.1 complete | ⚡ Yes |
| **A.12.1** | Operating procedures | 8-10 | $10K-15K | Multiple dependencies | No |
| **A.12.2** | Change management | 6-8 | $10K-20K | Tool selection | No |
| **A.12.7** | Information backup | 2-3 | $5K-10K | None | ⚡ Yes (cloud backup) |
| **A.12.8** | Event logging | 3-4 | $10K-25K | SIEM selection | ⚡ Yes (cloud-native) |
| **A.15.1** | Supplier security policy | 3-4 | $5K-10K | A.5.1 complete | No |
| **A.15.2** | Supplier agreements | 8-12 | $15K-30K | Legal review | No |
| **A.15.4** | Supplier monitoring | 4-6 | $5K-10K | A.15.2 complete | No |
| **A.16.1** | Incident mgmt procedures | 6-8 | $10K-20K | Team designation | No |
| **A.16.2** | Reporting events | 2-3 | $2K-5K | A.16.1 complete | ⚡ Yes |
| **A.16.5** | Incident response | 6-8 | $15K-30K | A.16.1, training | No |
| **A.17.1** | BC planning | 8-10 | $15K-30K | BIA complete | No |
| **A.17.2** | BC implementation | 6-8 | $10K-25K | A.17.1 complete | No |
| **A.18.1** | Compliance register | 2-3 | $2K-5K | Legal review | ⚡ Yes |
| **A.6.1** | Security roles/responsibilities | 2-3 | $3K-5K | Org chart update | ⚡ Yes |
| **A.6.6** | Info sec in supplier relationships | 4-6 | $5K-10K | A.6.1, A.15.1 | No |
| **A.7.3** | Security awareness training | 3-4 | $5K-10K | Content selection | ⚡ Yes (platform) |
| **A.10.1** | Cryptographic controls | 2-3 | $2K-5K | None | ⚡ Yes (cloud encryption) |
| **A.14.1** | Security in development | 6-8 | $10K-20K | SDLC review | No |
| **A.13.1** | Network controls | 4-6 | $5K-15K | Network architecture | ⚡ Yes (cloud security groups) |

**P0 Totals:**
- **Total Effort:** 120-160 weeks (with parallelization: 6-8 months)
- **Total Cost:** $172K-345K
- **Quick Wins:** 11 controls (39%)
- **Cloud-Leverageable:** 8 controls (29%)

---

## P1 - High Priority Controls (35 Controls)

### High Risk or Essential for Robust ISMS

| Control | Description | Effort (Weeks) | Cost | Dependencies | Timeline |
|---------|-------------|----------------|------|--------------|----------|
| **A.6.2** | Segregation of duties | 3-4 | $3K-5K | A.6.1 | Month 4-6 |
| **A.6.5** | Info sec in project mgmt | 4-6 | $5K-10K | A.6.1 | Month 5-7 |
| **A.7.1** | Screening (background checks) | 2-3 | $2K-5K | HR process | Month 3-5 |
| **A.7.2** | Employment terms | 2-3 | $5K-10K | Legal review | Month 3-5 |
| **A.7.5** | Post-termination responsibilities | 1-2 | $1K-3K | HR process | Month 4-6 |
| **A.7.6** | NDAs and confidentiality | 2-3 | $3K-5K | Legal review | Month 3-5 |
| **A.8.2** | Ownership of assets | 2-3 | $2K-5K | A.8.1 | Month 5-7 |
| **A.8.3** | Acceptable use policy | 2-3 | $2K-5K | A.5.1 | Month 4-6 |
| **A.8.6** | Labeling of information | 3-4 | $3K-8K | A.8.5 | Month 6-8 |
| **A.8.7** | Handling of assets | 2-3 | $2K-5K | A.8.5 | Month 6-8 |
| **A.8.9** | Disposal of media | 2-3 | $3K-8K | Vendor selection | Month 5-7 |
| **A.8.10** | Information deletion | 2-3 | $2K-5K | A.8.9 | Month 6-8 |
| **A.9.4** | User authentication mgmt | 3-4 | $5K-15K | A.9.1 | Month 4-6 |
| **A.9.6** | Access restrictions | 4-6 | $5K-10K | A.9.1 | Month 5-7 |
| **A.11.7** | Clear desk/clear screen | 1-2 | $1K-2K | A.5.3 | Month 6-8 |
| **A.12.3** | Capacity management | 3-4 | $5K-10K | Monitoring tools | Month 7-9 |
| **A.12.4** | Dev/test/prod separation | 4-6 | $10K-25K | Infrastructure | Month 6-8 |
| **A.12.9** | Administrator logs | 2-3 | $3K-8K | A.12.8 | Month 6-8 |
| **A.12.10** | Clock synchronization | 1 | $1K-2K | None | Month 6-8 |
| **A.13.2** | Security of network services | 3-4 | $5K-10K | A.13.1 | Month 6-8 |
| **A.13.3** | Network segregation | 4-6 | $10K-20K | A.13.1 | Month 7-9 |
| **A.13.4** | Information transfer policies | 2-3 | $3K-5K | A.5.3 | Month 6-8 |
| **A.13.5** | Electronic messaging security | 2-3 | $5K-10K | Email security | Month 5-7 |
| **A.14.2** | Securing app services | 4-6 | $10K-20K | A.14.1 | Month 8-10 |
| **A.14.3** | Protecting transactions | 3-4 | $5K-15K | A.14.1 | Month 8-10 |
| **A.14.5** | Security in development | 6-8 | $10K-25K | SDLC | Month 7-9 |
| **A.14.8** | Security testing | 4-6 | $10K-20K | Testing tools | Month 9-11 |
| **A.15.3** | ICT supply chain | 4-6 | $5K-15K | A.15.1 | Month 7-9 |
| **A.15.5** | Supplier change mgmt | 2-3 | $3K-5K | A.15.4 | Month 8-10 |
| **A.16.3** | Reporting weaknesses | 1-2 | $1K-3K | A.16.1 | Month 7-9 |
| **A.16.7** | Collection of evidence | 2-3 | $5K-10K | A.16.1 | Month 8-10 |
| **A.17.3** | BC verification/testing | 3-4 | $5K-15K | A.17.2 | Month 10-12 |
| **A.18.2** | Intellectual property | 2-3 | $3K-5K | Legal review | Month 7-9 |
| **A.18.4** | Privacy and PII protection | 4-6 | $10K-20K | Privacy assessment | Month 6-8 |
| **A.18.7** | Compliance with policies | 2-3 | $3K-5K | Internal audit | Month 9-11 |

**P1 Totals:**
- **Total Effort:** 95-130 weeks (with parallelization: 5-7 months)
- **Total Cost:** $151K-316K
- **Overlaps with P0:** Can execute concurrently in months 4-10

---

## P2 - Medium Priority Controls (22 Controls)

### Required but Partial Implementation Acceptable Initially

| Control | Description | Effort (Weeks) | Cost | Timeline |
|---------|-------------|----------------|------|----------|
| **A.6.3** | Contact with authorities | 1 | $500-1K | Month 8-10 |
| **A.6.4** | Special interest groups | 1 | $500-1K | Month 8-10 |
| **A.6.7** | Supplier agreement monitoring | 2-3 | $3K-5K | Month 9-11 |
| **A.7.4** | Disciplinary process | 2-3 | $2K-5K | Month 8-10 |
| **A.8.4** | Return of assets | 1-2 | $1K-3K | Month 8-10 |
| **A.8.8** | Removable media mgmt | 2-3 | $3K-8K | Month 9-11 |
| **A.8.11** | Data masking | 3-4 | $5K-15K | Month 10-12 |
| **A.8.12** | Data leakage prevention | 4-6 | $15K-40K | Month 10-12 |
| **A.11.1-11.14** | Physical security controls (14 total) | 2-8 | $10K-50K | Month 8-12 |
| **A.12.5** | Test data protection | 2-3 | $3K-5K | Month 9-11 |
| **A.12.6** | Configuration management | 4-6 | $10K-20K | Month 9-11 |
| **A.12.11** | Log protection | 2-3 | $3K-8K | Month 9-11 |
| **A.12.12** | Log analysis | 3-4 | $5K-15K | Month 10-12 |
| **A.12.13** | Software installation controls | 2-3 | $5K-10K | Month 10-12 |
| **A.12.14** | System audit considerations | 2-3 | $3K-5K | Month 10-12 |
| **A.13.6** | Technical vulnerability mgmt | 4-6 | $10K-25K | Month 9-11 |
| **A.14.4** | Security in support processes | 3-4 | $5K-10K | Month 10-12 |
| **A.14.9** | System change control | 3-4 | $5K-10K | Month 10-12 |
| **A.14.12** | Secure engineering principles | 4-6 | $5K-15K | Month 11-13 |
| **A.17.4** | Availability of facilities | 3-4 | $5K-15K | Month 11-13 |
| **A.18.3** | Protection of records | 2-3 | $3K-8K | Month 10-12 |
| **A.18.6** | Independent security review | 2-3 | $5K-10K | Month 11-12 |

**P2 Totals:**
- **Total Effort:** 56-85 weeks (with parallelization: 4-6 months)
- **Total Cost:** $111K-283K
- **Timeline:** Months 8-13 (overlapping with P0/P1 completion)

---

## P3 - Low Priority Controls (8 Controls)

### Can Be Deferred to Post-Certification

| Control | Description | Effort (Weeks) | Cost | Timeline |
|---------|-------------|----------------|------|----------|
| **A.12.15** | Software installation restrictions | 2-3 | $3K-8K | Post-cert |
| **A.13.7** | Network connection control | 3-4 | $5K-15K | Post-cert |
| **A.14.6** | Secure development standards | 4-6 | $10K-20K | Post-cert |
| **A.14.7** | Secure coding practices | 6-8 | $10K-25K | Post-cert |
| **A.14.10** | Technical reviews | 2-3 | $5K-10K | Post-cert |
| **A.14.11** | Restrictions on package changes | 2-3 | $3K-8K | Post-cert |
| **A.14.13** | Test data protection (advanced) | 3-4 | $5K-15K | Post-cert |
| **A.18.5** | Cryptographic regulation | 1-2 | $2K-5K | Post-cert |

**P3 Totals:**
- **Total Effort:** 23-33 weeks
- **Total Cost:** $43K-106K
- **Timeline:** Post-certification continuous improvement

---

## Quick Win Opportunities Summary

### High-Impact, Low-Effort Controls (Complete in Weeks 1-8)

| # | Control | Description | Effort | Cost | Impact |
|---|---------|-------------|--------|------|--------|
| 1 | **A.10.1** | Enable cloud encryption | 1 week | $1K-2K | ⭐⭐⭐⭐⭐ |
| 2 | **A.12.7** | Enable cloud backups | 1 week | $2K-5K | ⭐⭐⭐⭐⭐ |
| 3 | **A.12.8** | Enable cloud logging | 1 week | $3K-8K | ⭐⭐⭐⭐⭐ |
| 4 | **A.13.1** | Configure security groups | 1 week | $1K-3K | ⭐⭐⭐⭐ |
| 5 | **A.9.5** | Conduct access review | 2 weeks | $2K-5K | ⭐⭐⭐⭐⭐ |
| 6 | **A.9.2** | Enable MFA | 1 week | $3K-8K | ⭐⭐⭐⭐⭐ |
| 7 | **A.5.1** | Policy from templates | 4 weeks | $5K-10K | ⭐⭐⭐⭐⭐ |
| 8 | **A.5.2** | Policy review schedule | 1 week | $1K-2K | ⭐⭐⭐ |
| 9 | **A.6.1** | Define security roles | 2 weeks | $3K-5K | ⭐⭐⭐⭐ |
| 10 | **A.7.3** | Security awareness platform | 2 weeks | $5K-10K | ⭐⭐⭐⭐ |
| 11 | **A.16.2** | Incident reporting process | 1 week | $2K-5K | ⭐⭐⭐⭐ |
| 12 | **A.18.1** | Create compliance register | 2 weeks | $2K-5K | ⭐⭐⭐⭐ |

**Quick Wins Total:**
- **Effort:** 19 weeks (can parallelize to 6-8 weeks)
- **Cost:** $30K-68K
- **Controls Implemented:** 12 (13% of total)
- **Risk Reduction:** ~40% of critical risks addressed
- **Timeline:** Weeks 1-8

**ROI:** Maximum risk reduction per dollar spent

---

## Cloud Provider Leverage Strategy

### Controls Inherited from AWS/Azure/GCP ISO 27001 Certification

| Control Category | Inherited Controls | Effort Savings | Cost Savings |
|------------------|-------------------|----------------|--------------|
| **Physical Security** (A.11) | 12/14 controls | 8-10 weeks | $10K-50K |
| **Cryptography** (A.10) | 1/1 controls | 2 weeks | $5K-15K |
| **Network Security** (A.13.1-13.3) | 2/7 controls | 4-6 weeks | $10K-25K |
| **Operations Security** (A.12.7-12.8) | 2/15 controls | 3-4 weeks | $10K-20K |
| **Availability** (A.17.4) | 1/1 controls | 2-3 weeks | $5K-15K |
| **Environmental** (A.11.5, A.11.11) | 2/14 controls | 2-4 weeks | $5K-20K |

**Total Cloud Leverage:**
- **Controls Inherited:** 20/93 (22%)
- **Effort Savings:** 21-31 weeks (4-6 months)
- **Cost Savings:** $45K-145K
- **Condition:** Proper shared responsibility documentation + attestation acquisition

**Action Required:**
1. Obtain cloud provider ISO 27001 certificates (free, request from provider)
2. Document shared responsibility model (1-2 weeks)
3. Map provider controls to Annex A requirements (2-3 weeks)
4. Include in Statement of Applicability (SoA)

---

## Phased Implementation Timeline

### Phase 1: Quick Wins & Foundation (Months 1-3)

**Focus:** Immediate risk reduction + foundational governance

**Controls to Complete (P0 Quick Wins):**
- A.5.1, A.5.2 (Policies)
- A.6.1 (Roles)
- A.7.3 (Awareness)
- A.9.2, A.9.5 (Access control)
- A.10.1 (Encryption)
- A.12.7, A.12.8 (Backup & logging)
- A.13.1 (Network controls)
- A.16.2 (Incident reporting)
- A.18.1 (Compliance register)

**Deliverables:**
- 12 controls implemented (13%)
- 8-12 core security policies approved
- MFA deployed organization-wide
- Asset inventory 50% complete
- Cloud provider attestations obtained

**Resources:**
- vCISO: 0.5 FTE
- IT/Security Analyst: 0.5 FTE
- Compliance Coordinator: 0.3 FTE
- External consultant: $10K-15K

**Cost:** $45K-75K

---

### Phase 2: Core Controls (Months 4-8)

**Focus:** Critical and high-priority control implementation

**Controls to Complete (Remaining P0 + High-Priority P1):**
- A.8.1, A.8.5 (Asset inventory & classification)
- A.9.1, A.9.3, A.9.4, A.9.6 (Access control framework)
- A.12.1, A.12.2 (Operations procedures & change mgmt)
- A.15.1, A.15.2, A.15.4 (Supplier security)
- A.16.1, A.16.5 (Incident response)
- A.17.1, A.17.2 (Business continuity)
- A.14.1, A.14.2, A.14.3 (Secure development)
- Plus 20-25 P1 controls

**Deliverables:**
- 70-75 controls implemented (75-80%)
- All critical risks mitigated
- Incident response plan tested
- BCP/DRP documented
- All suppliers assessed

**Resources:**
- vCISO: 0.5 FTE
- IT/Security Analyst: 0.7 FTE
- Compliance Coordinator: 0.5 FTE
- External consultant: $20K-40K

**Cost:** $80K-130K

---

### Phase 3: Certification Preparation (Months 9-12)

**Focus:** Complete remaining controls + audit preparation

**Controls to Complete (Remaining P1 + P2):**
- Remaining P1 controls (5-10)
- P2 controls as needed
- Address any gaps identified in internal audit

**Deliverables:**
- 93/93 controls implemented (100%)
- Clean internal audit
- Stage 1 audit complete
- Stage 2 audit complete
- ISO 27001 certification achieved

**Resources:**
- vCISO: 0.5 FTE
- IT/Security Analyst: 0.5 FTE
- Compliance Coordinator: 0.5 FTE
- External consultant: $10K-20K
- Certification audit: $25K-50K

**Cost:** $55K-95K

---

### Phase 4: Post-Certification (Months 13+)

**Focus:** Continuous improvement + surveillance audits

**Controls to Complete (P3):**
- Advanced security capabilities
- Process maturation
- Additional certifications (if needed)

**Deliverables:**
- Successful surveillance audits
- Enhanced security posture
- Additional certifications (SOC 2, etc.)

**Resources:**
- Security Manager: 0.5 FTE
- IT/Security Analyst: 0.3 FTE
- Compliance Coordinator: 0.2 FTE
- Surveillance audit: $10K-15K/year

**Annual Cost:** $120K-200K

---

## Critical Path Dependencies

### Must Complete Before Others Can Start

```
A.5.1 (Policy) → A.5.3 (Topic policies) → Most other controls
                ↓
                A.6.1 (Roles) → A.9.1 (Access policy) → A.9.2-9.6 (Access controls)
                                                     → A.15.1 (Supplier policy) → A.15.2-15.5
                                                     → A.16.1 (Incident policy) → A.16.2-16.7

A.8.1 (Asset inventory) → A.8.5 (Classification) → A.8.6-8.12 (Handling controls)

A.12.1 (Operating procedures) → A.12.2-12.15 (Operations controls)

A.14.1 (Secure SDLC) → A.14.2-14.13 (Development controls)

A.17.1 (BC planning) → A.17.2-17.4 (BC implementation & testing)
```

**Critical Path Timeline:** 8-10 months (parallel execution possible)

---

## Success Metrics & KPIs

### Month 3 Milestones
- ✅ 12+ controls implemented (13%)
- ✅ All quick wins completed
- ✅ Cloud provider attestations obtained
- ✅ MFA deployment 100%
- ✅ Asset inventory 50% complete

### Month 8 Milestones
- ✅ 70-75 controls implemented (75-80%)
- ✅ All P0 controls complete
- ✅ Internal audit completed
- ✅ Major findings remediated
- ✅ Pre-audit assessment complete

### Month 12 Milestones
- ✅ 93 controls implemented (100%)
- ✅ Stage 1 audit passed
- ✅ Stage 2 audit passed
- ✅ ISO 27001 certification achieved
- ✅ Zero critical findings

### Continuous Improvement
- Annual surveillance audits passed
- Security incident metrics tracking
- Continuous compliance monitoring
- Regular management reviews

---

## Cost Optimization Strategies

### Strategy 1: Maximize Cloud Leverage (30% savings)
- Use cloud-native security controls
- Obtain and map provider certifications
- Reduce custom implementation
- **Savings:** $45K-145K

### Strategy 2: Template Utilization (40% savings)
- Use ISO 27001 policy templates
- Leverage industry frameworks (NIST, CIS)
- Adapt vs. create from scratch
- **Savings:** $30K-80K

### Strategy 3: Virtual CISO (50% savings)
- Fractional expertise vs. full-time hire
- Scale up/down as needed
- Transition to internal when justified
- **Savings:** $70K-100K/year

### Strategy 4: Open Source & SaaS Tools (60% savings)
- Avoid enterprise-grade tools initially
- Use cloud-native services
- Open source where appropriate
- **Savings:** $50K-100K

### Strategy 5: Phased Approach (Risk-Based)
- Focus on critical controls first
- Defer nice-to-haves
- Partial implementation where acceptable
- **Savings:** Time to market (3-6 months earlier)

**Total Potential Savings:** $195K-425K
**Optimized Budget:** $180K-280K (vs. $375K-705K full cost)

---

## Risk Mitigation Checkpoints

### Month 3 Checkpoint
- **Gate Criteria:** Quick wins complete, policies approved, vCISO engaged
- **Risk if Not Met:** Timeline extends 2-3 months
- **Mitigation:** Executive escalation, resource reallocation

### Month 8 Checkpoint
- **Gate Criteria:** 75% controls implemented, clean internal audit
- **Risk if Not Met:** Certification delayed 3-6 months
- **Mitigation:** Bring in additional consulting support, scope reduction

### Month 12 Checkpoint
- **Gate Criteria:** 100% controls, Stage 1 audit passed
- **Risk if Not Met:** Additional audit cycles required ($$$)
- **Mitigation:** Pre-audit assessment, mock audit, remediation sprint

---

## Conclusion

This prioritized remediation plan provides a realistic, risk-based approach to ISO 27001 certification for a small B2B organization. By focusing on:

1. ✅ **Quick wins first** (13% of controls, 40% of risk, 6-8 weeks)
2. ✅ **Cloud provider leverage** (22% of controls inherited, 30% cost savings)
3. ✅ **Critical path management** (parallel execution where possible)
4. ✅ **Cost optimization** (50-60% savings through smart strategies)

The organization can achieve certification in **12-18 months** for **$180K-280K** instead of the typical **24+ months** and **$400K+** for organizations starting from scratch.

**Key to Success:**
- Executive commitment
- Dedicated security leadership (vCISO)
- Pragmatic scoping
- Template and framework utilization
- Realistic timeline expectations

This plan is achievable, affordable, and positions the organization for long-term security maturity beyond just compliance checkboxes.
