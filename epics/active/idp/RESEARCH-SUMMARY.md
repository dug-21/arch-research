# IDP Service Catalog Research - Executive Summary

**Date:** September 30, 2025
**Research Scope:** Integration of ACP concepts with IDP security

---

## TL;DR - Key Findings

1. **IDP Service Catalogs** use YAML-based metadata with ownership tracking and dependency management (Backstage, Port, Humanitec)
2. **Agentic Security** requires unique agent identities with JWT tokens (15-30 min expiry), OIDC auth, and comprehensive audit trails
3. **Time-Based Authorization** reduces attack surface through deployment windows and expiring credentials
4. **SLSA Framework** provides 4 progressive levels from basic provenance (L1) to hermetic builds (L4)
5. **Test Maturity** industry standard is 80% code coverage at TMMi Level 4 for deployment authorization

---

## ACP-IDP Integration Pattern

```
Developer → Service Catalog → Shopping Cart → Approval Workflow → Agentic Provisioning → Time-Limited Access
```

**Timeline:** 10-15 minutes (vs. 3-5 days traditional)

---

## Security Architecture Layers

| Layer | Implementation | Standard |
|-------|----------------|----------|
| **Identity** | Enterprise SSO + Agent Service Principals | OIDC/JWT |
| **Authorization** | RBAC + ABAC + TBAC | Time-based windows |
| **Provisioning** | Isolated builds, signed provenance | SLSA Level 3+ |
| **Quality** | Automated gates, 80% coverage | TMMi Level 4 |
| **Audit** | Immutable logs, temporal forensics | Full traceability |

---

## JWT Token Configuration

- **Access Tokens:** 15-30 minutes
- **Refresh Tokens:** 7-14 days (single-use rotation)
- **Strategy:** Two-token pattern (access + refresh)
- **Rotation:** Every exchange invalidates old tokens

---

## SLSA Levels Quick Reference

| Level | Key Requirement | Security Benefit |
|-------|----------------|------------------|
| **L1** | Automated provenance | Build transparency |
| **L2** | Signed provenance + hosted build | Tamper detection |
| **L3** | Isolated builds + unforgeable provenance | Insider attack prevention |
| **L4** | Hermetic builds + 2-person review | Maximum assurance |

---

## TMMi Test Maturity Levels

| Level | Name | Key Characteristics | Coverage Target |
|-------|------|-------------------|----------------|
| **L1** | Initial | Ad-hoc testing | Variable |
| **L2** | Managed | Project-level processes | 60-70% |
| **L3** | Defined | Organization-wide standards | 70-75% |
| **L4** | Measured | Quantitative quality gates | **80%+** |
| **L5** | Optimization | Continuous improvement | 85-95% |

---

## Quality Gate Standard Configuration

```yaml
quality_gates:
  code_coverage: ">= 80%"
  test_pass_rate: ">= 95%"
  critical_vulnerabilities: "0"
  high_vulnerabilities: "<= 3"
  performance_p95: "<= 500ms"
  two_person_review: "required_for_production"
```

---

## Agentic System Agent Types

1. **Catalog Agent** - Service discovery and metadata
2. **Policy Agent** - Authorization and approval workflows
3. **Provisioning Agent** - Infrastructure-as-code execution
4. **Security Agent** - Credential management and scanning
5. **Quality Agent** - Test execution and gate evaluation
6. **Audit Agent** - Immutable logging and forensics

---

## Implementation Roadmap

| Phase | Duration | Key Deliverables |
|-------|----------|-----------------|
| Foundation | Months 1-2 | Service catalog, basic RBAC, audit logs |
| Automation | Months 3-4 | Approval workflows, GitOps, initial agents |
| Security | Months 5-6 | JWT auth, SLSA L2, security gates |
| Quality | Months 7-8 | 80% coverage, SLSA L3, quality agents |
| Time Controls | Months 9-10 | Deployment windows, TTL, temporal audit |
| Full Integration | Months 11-12 | Complete "shopping cart", SLSA L4 |

---

## Success Metrics (12-month targets)

| Metric | Target |
|--------|--------|
| Provisioning Time | <30 minutes |
| Manual Approvals | <20% |
| Deployment Failures | <5% |
| Security Incidents (agentic) | 0 |
| Test Coverage | >80% |
| SLSA Compliance | Level 3+ |

---

## Critical Security Controls

### Agent Identity Management
- Each agent has unique service principal ID
- Credentials rotate every 15-30 minutes
- Workload identity federation enabled
- No shared secrets between agents

### Deployment Authorization
- Time-based windows (e.g., Tue/Thu 10am-2pm)
- Quality gates must pass (80% coverage, 95% pass rate)
- Budget and quota enforcement
- Approval workflow for sensitive resources

### Audit Trail Requirements
- Every agent action logged with full context
- Immutable audit log storage
- Temporal forensics for incident investigation
- Compliance-ready reporting

---

## Technology Stack Recommendations

**IDP Platform:** Backstage (open-source, extensible) or Port (commercial, turnkey)

**Code Signing:** Sigstore (automated, keyless signing)

**Provenance:** in-toto (standardized attestations)

**Distribution:** TUF (secure repository management)

**Authentication:** OIDC with enterprise IdP (Entra ID, Okta)

**Tokens:** JWT with short expiry + refresh token rotation

**Testing:** TMMi Level 4 framework with 80% coverage gates

**Supply Chain:** SLSA Level 3 minimum (Level 4 for critical services)

---

## Risk Mitigation Summary

| Risk | Mitigation | Effectiveness |
|------|-----------|---------------|
| Agent compromise | 15-30 min credentials + rotation | High |
| Insufficient quality | TMMi L4 + 80% coverage gates | High |
| Over-permissioned access | RBAC + ABAC + TBAC layers | High |
| Supply chain attacks | SLSA L3+ + Sigstore + in-toto | Very High |
| Audit gaps | Immutable logs + temporal forensics | High |

---

## Next Steps

1. Review full research document: `RESEARCH-IDP-SERVICE-CATALOG.md`
2. Select IDP platform (Backstage vs. Port vs. Humanitec)
3. Design service catalog schema (YAML metadata structure)
4. Define initial quality gates (start with TMMi L2)
5. Prototype agentic provisioning agent with JWT auth
6. Implement SLSA Level 2 (signed provenance)

---

**Full Research Document:** `/Users/dmf/repos/arch-research/epics/active/idp/RESEARCH-IDP-SERVICE-CATALOG.md`

**Research Status:** ✅ Complete
**Swarm Coordination:** ✅ All findings stored in distributed memory
**Next Review:** December 30, 2025
