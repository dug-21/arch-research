# Leveraging Cloud Provider ISO 27001 Certifications

## Overview

Your organization can **inherit approximately 35-40% of ISO 27001 Annex A controls** from cloud providers (AWS, Azure, Google Cloud). This significantly reduces your implementation effort and cost.

**Key Principle**: Shared Responsibility Model - Cloud providers secure the infrastructure, you secure your use of that infrastructure.

---

## Shared Responsibility Model

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR RESPONSIBILITY                       │
│  - Data classification and handling                          │
│  - Identity and access management (IAM)                      │
│  - Application security                                      │
│  - Cloud configuration security                              │
│  - Encryption key management (if you manage keys)           │
│  - Network security (security groups, network ACLs)          │
│  - Monitoring and logging (enable and review)               │
│  - Incident response (detect, respond, recover)              │
│  - Backup management (if not using managed backups)         │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│              CLOUD PROVIDER RESPONSIBILITY                   │
│  - Physical data center security                             │
│  - Hardware and infrastructure security                      │
│  - Hypervisor and virtualization security                    │
│  - Network infrastructure security                           │
│  - Managed service security (for PaaS/SaaS)                 │
│  - Environmental controls (power, cooling, fire suppression)│
│  - Redundancy and availability (infrastructure)              │
│  - Infrastructure patch management                           │
└─────────────────────────────────────────────────────────────┘
```

**Your Task**: Document and verify what the cloud provider does, then implement YOUR responsibilities.

---

## Cloud Provider Compliance Reports

### Where to Find Them

**AWS**:
- AWS Artifact (in AWS Console): ISO 27001, SOC 2, PCI DSS, HIPAA, many others
- https://aws.amazon.com/compliance/
- Download ISO 27001 certificate and SOC 2 Type II report

**Microsoft Azure**:
- Service Trust Portal: https://servicetrust.microsoft.com/
- ISO 27001, SOC 2, FedRAMP, many others
- Download Azure compliance reports

**Google Cloud**:
- Compliance Reports Manager (in GCP Console)
- https://cloud.google.com/security/compliance
- ISO 27001, SOC 2, PCI DSS, many others

**Other Cloud/SaaS Providers**:
- Request compliance reports from vendor
- Most reputable SaaS providers have ISO 27001 or SOC 2
- If vendor can't provide, consider if they're appropriate for sensitive data

---

### How to Use Compliance Reports in Your ISMS

1. **Download Reports**:
   - ISO 27001 certificates (public)
   - SOC 2 Type II reports (may require NDA)
   - Audit reports and attestations

2. **Review Reports**:
   - Verify scope (which services are covered?)
   - Review control descriptions (what does provider do?)
   - Identify your responsibilities (what do you need to do?)

3. **Document in Your ISMS**:
   - Reference provider compliance in your Statement of Applicability (SOA)
   - Example: "A.7.1 Physical Security Perimeters - Implemented by AWS, verified via ISO 27001 certificate dated [date]"
   - Store compliance reports as evidence

4. **Monitor Ongoing**:
   - Check for updated compliance reports annually
   - Monitor for provider security incidents
   - Review provider security bulletins

---

## Annex A Controls You Can Inherit

### Fully Inherited (Provider Implements, You Document)

| Control | Description | Cloud Provider Responsibility | Your Action |
|---------|-------------|------------------------------|-------------|
| **A.7.1** | Physical Security Perimeters | Data center perimeter fencing, barriers, guards | Download ISO 27001 cert, reference in SOA |
| **A.7.2** | Physical Entry | Data center access control, biometrics, mantraps | Download ISO 27001 cert, reference in SOA |
| **A.7.3** | Securing Offices, Rooms, Facilities | Data center physical security design | Download ISO 27001 cert, reference in SOA |
| **A.7.4** | Physical Security Monitoring | 24/7 video surveillance, security operations center | Download ISO 27001 cert, reference in SOA |
| **A.7.5** | Protecting Against Physical/Environmental Threats | Fire suppression, HVAC, flood protection, UPS, generators | Download ISO 27001 cert, reference in SOA |
| **A.7.8** | Equipment Siting and Protection | Data center environmental controls, equipment protection | Download ISO 27001 cert, reference in SOA |
| **A.7.11** | Supporting Utilities | Redundant power, cooling, network connectivity | Download ISO 27001 cert, reference in SOA |
| **A.7.12** | Cabling Security | Secure cable routing, redundant cabling | Download ISO 27001 cert, reference in SOA |
| **A.7.13** | Equipment Maintenance | Infrastructure maintenance (provider equipment) | Download ISO 27001 cert, reference in SOA |
| **A.7.14** | Secure Disposal or Re-Use | Infrastructure equipment disposal (cryptographic erasure) | Download ISO 27001 cert, reference in SOA |

**Total Fully Inherited**: ~10 controls (all physical controls for cloud infrastructure)

---

### Partially Inherited (Provider Provides Tools, You Configure)

| Control | Description | Cloud Provider Provides | Your Responsibility |
|---------|-------------|------------------------|---------------------|
| **A.5.23** | Cloud Security | Certified cloud infrastructure, security features | Configure security properly, understand shared responsibility |
| **A.8.1** | Endpoint Security | Cloud-based MDM (Intune, Jamf) | Deploy MDM, enroll devices, configure policies |
| **A.8.6** | Capacity Management | Elastic scaling, auto-scaling groups | Configure auto-scaling, monitor usage, plan capacity |
| **A.8.7** | Malware Protection | Cloud anti-malware tools (AWS GuardDuty, Azure Defender) | Enable tools, configure alerts, respond to detections |
| **A.8.8** | Vulnerability Management | Cloud vulnerability scanning (AWS Inspector, Azure Security Center) | Enable scanning, review results, remediate vulnerabilities |
| **A.8.9** | Configuration Management | Cloud config management (AWS Config, Azure Policy, Terraform) | Define baselines, implement config-as-code, monitor drift |
| **A.8.13** | Backup | Cloud backup services (AWS Backup, Azure Backup) | Configure backups, set retention, test restores |
| **A.8.14** | Redundancy | Multi-region deployment, load balancing, database replication | Design multi-region architecture, configure failover |
| **A.8.15** | Logging | Cloud logging services (CloudTrail, Azure Monitor, Cloud Logging) | Enable logging, configure retention, protect log integrity |
| **A.8.16** | Monitoring | Cloud SIEM (AWS Security Hub, Azure Sentinel, GCP SCC) | Configure monitoring, set up alerts, review events |
| **A.8.17** | Clock Synchronization | NTP automatically configured in cloud | Verify time sync, ensure consistency |
| **A.8.20** | Network Security | VPCs, security groups, network ACLs, firewalls | Configure network segmentation, least-privilege firewall rules |
| **A.8.22** | Network Segregation | VPCs, subnets, separate accounts | Design network architecture, implement segregation |
| **A.8.24** | Cryptography | Cloud key management (AWS KMS, Azure Key Vault, GCP KMS) | Enable encryption, manage keys, configure TLS/SSL |

**Total Partially Inherited**: ~14 controls

---

### Your Office Physical Controls (Not Cloud-Applicable)

These apply to your office, not cloud infrastructure:

| Control | Your Implementation | Effort |
|---------|-------------------|--------|
| **A.7.1-A.7.5** (Office) | Basic office physical security (locked doors, visitor log) | Low |
| **A.7.6** | Secure areas (if you have data centers/server rooms) | Low (likely N/A for cloud-only) |
| **A.7.7** | Clear desk/clear screen | Clean desk policy, auto screen lock | Low |
| **A.7.9** | Off-premises assets | Laptop encryption, MDM, remote wipe | Medium (use cloud tools) |
| **A.7.10** | Storage media | Secure disposal of USB drives, hard drives | Low |

---

## Cloud-Specific Implementation Guidance

### AWS-Specific Recommendations

**High-Value Services to Enable**:

1. **AWS CloudTrail**: Audit logging (all API calls)
   - Enable in all regions
   - Log to S3 with versioning and MFA delete
   - **Cost**: Included (S3 storage costs only)

2. **AWS GuardDuty**: Threat detection (malware, anomalies)
   - Enable in all regions
   - Configure SNS alerts for findings
   - **Cost**: ~$5-20/month depending on usage

3. **AWS Config**: Configuration monitoring and compliance
   - Enable in all regions
   - Use conformance packs (CIS AWS Foundations Benchmark)
   - **Cost**: ~$2/config item/region/month

4. **AWS Security Hub**: Centralized security findings
   - Aggregates GuardDuty, Config, Inspector, Macie
   - **Cost**: ~$0.0010 per 10,000 findings

5. **AWS Systems Manager**: Patch management
   - Automate OS patching
   - **Cost**: Included

6. **AWS Backup**: Automated backups
   - Centralized backup management
   - **Cost**: Storage + backup requests (~$0.05/GB-month)

7. **AWS Secrets Manager or Parameter Store**: Secrets management
   - Store API keys, database passwords
   - **Cost**: Secrets Manager (~$0.40/secret/month), Parameter Store (free tier)

8. **AWS KMS**: Encryption key management
   - Manage encryption keys, enable encryption at rest
   - **Cost**: $1/key/month + API requests

**Total Monthly Cost** (for typical small-medium workload): $50-200/month

---

### Azure-Specific Recommendations

**High-Value Services to Enable**:

1. **Azure Activity Log**: Audit logging (control plane)
   - Always enabled (free)
   - Export to Log Analytics for retention

2. **Azure Defender (Microsoft Defender for Cloud)**: Security monitoring
   - Enable for VMs, storage, databases, containers
   - **Cost**: ~$15/VM/month, varies by service

3. **Azure Policy**: Compliance and governance
   - Built-in policies for CIS benchmarks, ISO 27001
   - **Cost**: Included

4. **Azure Security Center**: Centralized security view
   - Free tier (basic recommendations), paid tier (advanced threat protection)
   - **Cost**: Free to ~$15/VM/month

5. **Azure Backup**: Managed backup service
   - VM backups, database backups
   - **Cost**: ~$10/protected instance + storage

6. **Azure Monitor**: Logging and monitoring
   - Collect logs, set alerts
   - **Cost**: Pay-as-you-go (GB ingested)

7. **Azure Key Vault**: Secrets and key management
   - Store secrets, certificates, keys
   - **Cost**: ~$0.03/10,000 operations

8. **Azure Sentinel**: Cloud-native SIEM (optional)
   - Advanced threat detection, SOAR
   - **Cost**: ~$2/GB ingested

**Total Monthly Cost**: $100-500/month depending on VMs and services

---

### Google Cloud-Specific Recommendations

**High-Value Services to Enable**:

1. **Cloud Audit Logs**: Audit logging
   - Admin activity logs (always enabled, free)
   - Data access logs (enable, costs for storage)
   - **Cost**: Storage costs only

2. **Security Command Center (SCC)**: Security monitoring
   - Standard tier (free), Premium tier (threat detection)
   - **Cost**: Free (standard) to ~$75/project/month (premium)

3. **Cloud Asset Inventory**: Asset visibility
   - Track all resources
   - **Cost**: Included

4. **Cloud Key Management (Cloud KMS)**: Encryption key management
   - Manage encryption keys
   - **Cost**: $0.06/key version/month + operations

5. **Secret Manager**: Secrets management
   - Store API keys, passwords
   - **Cost**: $0.06/secret version/month + operations

6. **Cloud Armor**: Web application firewall (WAF)
   - Protect against DDoS, OWASP Top 10
   - **Cost**: $5/policy/month + rules

7. **VPC Service Controls**: Network security perimeters
   - Advanced network security
   - **Cost**: Included

**Total Monthly Cost**: $50-300/month

---

## Statement of Applicability (SOA) - How to Document Inherited Controls

### Template for Inherited Controls

```
Control: A.7.1 - Physical Security Perimeters

Applicability: Implemented by Cloud Provider

Implementation:
[Company] uses AWS for cloud infrastructure. AWS data centers implement
physical security perimeters including:
- Perimeter fencing and barriers
- Security guards and 24/7 monitoring
- Multiple security layers
- Intrusion detection systems

Evidence:
- AWS ISO 27001 Certificate (Scope: AWS Infrastructure, Valid through: [Date])
- AWS SOC 2 Type II Report (Date: [Date])
- AWS Compliance Documentation (stored in ISMS repository)

[Company] Responsibilities:
- Annual review of AWS compliance reports (due: [Date])
- Monitor AWS security bulletins for incidents
- Ensure AWS services used are within scope of AWS ISO 27001 certification

Verification:
- AWS ISO 27001 certificate reviewed and current: [Date]
- Shared responsibility model documented: [Date]
- AWS security bulletins monitored: Quarterly

Status: Implemented (via AWS)
Last Reviewed: [Date]
Next Review: [Date]
```

---

### Template for Partially Inherited Controls

```
Control: A.8.15 - Logging

Applicability: Partially Implemented (Shared Responsibility)

Implementation:
Cloud Provider Responsibility (AWS):
- AWS provides CloudTrail for API audit logging
- AWS provides VPC Flow Logs for network logging
- AWS provides CloudWatch Logs for application logging
- AWS infrastructure logging (certified via ISO 27001)

[Company] Responsibility:
- Enable CloudTrail in all AWS regions
- Configure log retention (1 year minimum)
- Enable log file integrity validation
- Protect log storage (S3 bucket versioning, MFA delete)
- Enable VPC Flow Logs
- Configure CloudWatch Logs for applications
- Review logs for security events

Evidence:
- Cloud logging policy (Date: [Date])
- CloudTrail configuration (all regions enabled, screenshot)
- Log retention configuration (S3 lifecycle policy)
- VPC Flow Logs enabled (screenshot)
- AWS ISO 27001 certificate (infrastructure logging)
- Log review records (monthly)

Status: Implemented
[Company] Configured: [Date]
AWS Certified: Verified [Date] via ISO 27001 cert
Last Reviewed: [Date]
Next Review: [Date]
```

---

## Audit Evidence: Cloud Provider Controls

### What to Collect

1. **Compliance Certificates**:
   - ISO 27001 certificates (AWS, Azure, GCP)
   - SOC 2 Type II reports
   - Other relevant certifications (PCI DSS, HIPAA, FedRAMP)

2. **Configuration Screenshots**:
   - Show that you've enabled cloud security features
   - GuardDuty/Defender/SCC enabled
   - CloudTrail/Activity Logs enabled
   - Encryption enabled
   - Backup configured

3. **Shared Responsibility Documentation**:
   - Document understanding of shared responsibility
   - List your responsibilities vs. provider responsibilities
   - Show how you've met YOUR responsibilities

4. **Monitoring Records**:
   - Provider security bulletins reviewed (quarterly)
   - Compliance report updates checked (annually)
   - Security incidents from provider (if any, and your response)

---

### What Auditors Will Ask

**Question**: "How do you ensure the cloud provider meets security requirements?"

**Answer**:
"We use [AWS/Azure/GCP] which holds ISO 27001 certification. We have verified their compliance through:
1. ISO 27001 certificate review (valid through [date])
2. SOC 2 Type II report review (dated [date])
3. Shared responsibility model documented in our ISMS
4. Quarterly monitoring of provider security bulletins
5. Annual review of updated compliance reports

We have configured our use of cloud services according to security best practices and enabled all relevant security features (CloudTrail, GuardDuty, encryption, etc.). Evidence is available in our ISMS documentation."

**Evidence to Show**:
- Provider compliance certificates
- Shared responsibility matrix
- Configuration screenshots (security features enabled)
- Monitoring records (bulletins reviewed, compliance reports checked)

---

## Annual Cloud Provider Compliance Monitoring

### Quarterly Tasks (15-30 minutes)

1. Review cloud provider security bulletins
2. Check for new security features (enable if relevant)
3. Monitor for provider security incidents
4. Review own cloud security configurations (scan for drift)

### Annual Tasks (2-4 hours)

1. Download updated compliance reports (ISO 27001, SOC 2)
2. Verify certificates are still valid
3. Review for scope changes (new services covered? any exclusions?)
4. Update SOA if provider scope changed
5. Verify shared responsibility model is still accurate
6. Check for new security services (evaluate if needed)

### Evidence

- Cloud provider monitoring log (spreadsheet tracking reviews)
- Updated compliance reports collected annually
- Notes on any changes or actions taken

---

## Cost Savings from Leveraging Cloud Providers

### Implementation Cost Savings

**If you had to implement physical controls yourself**:
- Data center build-out: $500,000 - $2,000,000
- Physical security (guards, cameras, access control): $50,000-$150,000/year
- Environmental controls (HVAC, fire suppression): $100,000-$300,000
- Redundant power (UPS, generators): $50,000-$200,000
- Ongoing maintenance and monitoring: $100,000-$300,000/year

**By using cloud providers with ISO 27001**:
- Capital cost: $0 (pay-as-you-go)
- Physical security: Included in cloud pricing
- Compliance: Inherit provider certifications
- Effort: 1-2 days to document (vs. months to implement)

**Savings**: $500,000+ upfront, $100,000+ annually

---

### Audit Cost Savings

**Without cloud provider certifications**:
- More controls to implement and test yourself
- More evidence to collect
- Longer audit duration
- Higher audit fees

**With cloud provider certifications**:
- ~40% fewer controls to implement
- Simpler evidence (reference provider certs)
- Faster audit (less to review)
- Lower audit fees (~20-30% reduction)

**Savings**: $5,000-$15,000 in audit fees

---

## Multi-Cloud Environments

**If you use multiple cloud providers** (e.g., AWS + Azure + Google Cloud):

1. **Collect compliance reports from each provider**
2. **Document shared responsibility for each provider**
3. **Ensure consistent security configurations** (e.g., logging, encryption, access control)
4. **Centralized monitoring** (aggregate logs from all providers)
5. **Unified policies** (single cloud security policy covering all providers)

**Effort**: +20-30% additional effort for multi-cloud (more complexity)

---

## SaaS Applications (Microsoft 365, Google Workspace, Salesforce, etc.)

### How to Leverage SaaS Provider Compliance

Same approach as cloud infrastructure:

1. **Verify compliance**:
   - Microsoft 365: ISO 27001, SOC 2 (Service Trust Portal)
   - Google Workspace: ISO 27001, SOC 2 (Compliance Reports Manager)
   - Salesforce: ISO 27001, SOC 2 (Trust.salesforce.com)
   - Other SaaS: Request compliance reports from vendor

2. **Configure security properly**:
   - Enable MFA
   - Configure access controls (least privilege)
   - Enable audit logging
   - Set data retention policies
   - Configure DLP (if available)

3. **Document in SOA**:
   - Reference SaaS provider compliance
   - Show you've configured security features
   - Monitor provider compliance annually

---

## Recommendation: Cloud Provider Leverage Checklist

### For Each Cloud Provider You Use:

- [ ] Download ISO 27001 certificate
- [ ] Download SOC 2 Type II report (if available)
- [ ] Review scope (which services are covered?)
- [ ] Document shared responsibility model
- [ ] Enable all relevant security services (logging, monitoring, encryption, etc.)
- [ ] Configure security per best practices (CIS Benchmarks)
- [ ] Reference provider compliance in your SOA
- [ ] Store compliance reports in ISMS repository
- [ ] Schedule annual review of provider compliance reports
- [ ] Schedule quarterly review of provider security bulletins

---

## Summary: Leveraging Cloud Provider Certifications

**Benefits**:
- **Inherit ~40% of Annex A controls** (physical, some infrastructure)
- **Reduce implementation effort** by 30-40%
- **Reduce implementation cost** by $500,000+ (no data center)
- **Accelerate time to certification** (less to implement)
- **Simplify audits** (reference provider certs)
- **Ongoing compliance** (provider maintains certifications)

**Your Responsibilities**:
- **Document** shared responsibility model
- **Configure** cloud security features properly
- **Enable** logging, monitoring, encryption, backups, etc.
- **Monitor** provider compliance annually
- **Reference** provider certifications in your SOA
- **Store** compliance reports as evidence

**Effort to Leverage**:
- Initial: 2-4 days (collect reports, document, configure)
- Ongoing: 3-4 hours/year (review updated reports)

**Cost**:
- Cloud security services: $50-500/month (depending on provider and usage)
- No additional cost for inheriting certifications

**Recommendation**: Fully leverage cloud provider ISO 27001 certifications. This is the single biggest effort and cost reducer for cloud-based organizations pursuing ISO 27001.
