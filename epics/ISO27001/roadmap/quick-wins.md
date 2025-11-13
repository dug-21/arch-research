# ISO 27001 Quick Wins Guide

## Overview

Quick Wins are high-impact, low-effort security controls that deliver immediate value while building momentum for your ISO 27001 program. Implement these in the first 1-3 months to:

- **Reduce risk immediately** (protect against common threats)
- **Build stakeholder confidence** (demonstrate progress)
- **Create momentum** (early wins motivate team and secure funding)
- **Deliver ROI fast** (measurable security improvements)

---

## Quick Win #1: Multi-Factor Authentication (MFA)

**Impact**: **CRITICAL** - Prevents 99.9% of account compromise attacks

**Effort**: 2-4 weeks

**Cost**: $2,000-$5,000 (implementation + user enrollment)

### Why This Matters

- Account compromise is the #1 entry point for breaches
- Stolen passwords are useless with MFA
- Required by ISO 27001 Annex A.5.17 and A.5.18
- Client expectation for B2B security

### Implementation Steps

**Week 1: Planning**
1. Choose MFA method:
   - **Recommended**: Authenticator app (Microsoft Authenticator, Google Authenticator, Authy)
   - **Acceptable**: SMS (less secure but better than nothing)
   - **Best**: Hardware security keys (YubiKey) for privileged accounts

2. Identify all systems requiring MFA:
   - Cloud services (AWS, Azure, Google Cloud)
   - Microsoft 365 / Google Workspace
   - SaaS applications (Salesforce, Slack, etc.)
   - VPN / remote access
   - Data rooms
   - Admin/privileged accounts (mandatory)

**Week 2-3: Rollout**
1. Pilot with IT team (test and refine process)
2. Create user enrollment guide (with screenshots)
3. Communicate to all staff (email, training session)
4. Department-by-department rollout
5. Helpdesk support for enrollment issues
6. Monitor enrollment progress

**Week 4: Enforcement**
1. Achieve 100% enrollment
2. Enforce MFA policy (disable MFA bypass)
3. Document exceptions (if any, with approval)
4. Report to management (completion, metrics)

### Success Metrics

- **100% of users enrolled in MFA**
- **Zero MFA bypass exceptions** (or minimal with executive approval)
- **Reduced account compromise attempts** (monitor failed MFA challenges)

### Evidence for Audit

- MFA policy
- MFA enrollment report (100%)
- Configuration screenshots (MFA enforced)
- User training records
- Management approval of exceptions (if any)

---

## Quick Win #2: Enable Audit Logging

**Impact**: **HIGH** - Enables incident detection and investigation

**Effort**: 1-2 weeks

**Cost**: $500-$2,000 (configuration, storage costs included in cloud)

### Why This Matters

- ISO 27001 Annex A.8.15 requires logging
- Detect security incidents in real-time
- Investigate incidents after the fact
- Compliance and audit evidence
- Cloud providers include logging for free (just need to enable and configure retention)

### Implementation Steps

**Week 1: Enable Logging**
1. **AWS**:
   - Enable CloudTrail (all regions, all events)
   - Enable VPC Flow Logs
   - Enable S3 access logging
   - Enable RDS database logging

2. **Azure**:
   - Enable Azure Activity Log
   - Enable NSG Flow Logs
   - Enable Storage Analytics Logging
   - Enable SQL Database Auditing

3. **Google Cloud**:
   - Enable Cloud Audit Logs
   - Enable VPC Flow Logs
   - Enable Cloud Storage access logs

4. **Microsoft 365 / Google Workspace**:
   - Enable audit logging
   - Enable mailbox auditing
   - Enable admin activity logging

5. **SaaS Applications**:
   - Enable audit logging in all SaaS apps (Salesforce, data rooms, etc.)

**Week 2: Configure Retention**
1. Set log retention to 1 year minimum (recommended)
2. Configure log storage (S3, Azure Blob, Google Cloud Storage)
3. Enable log integrity protection (immutable logs, versioning)
4. Test log collection (verify logs are being generated)

### Success Metrics

- **100% of in-scope systems** have logging enabled
- **Logs retained for 1+ years**
- **Log integrity protected** (immutable or versioned storage)

### Evidence for Audit

- Logging policy
- List of systems with logging enabled
- Log retention configuration
- Sample logs (demonstrate logging is working)
- Log storage configuration (immutability, retention)

---

## Quick Win #3: Verify and Test Backups

**Impact**: **CRITICAL** - Enables recovery from ransomware, data loss

**Effort**: 1-2 weeks

**Cost**: $1,000-$3,000 (testing, documentation; backup storage typically already in use)

### Why This Matters

- ISO 27001 Annex A.8.13 requires backups
- Ransomware is the #1 threat to businesses
- Data loss can be business-ending
- Backups are useless if they can't be restored
- Many organizations have backups but have never tested restore

### Implementation Steps

**Week 1: Verify Backups**
1. Inventory all critical systems and data:
   - Databases (client data, business data)
   - File storage (documents, data rooms)
   - Cloud configurations (infrastructure as code)
   - Email and collaboration tools

2. Verify backups are running:
   - Check backup schedules (daily? hourly? continuous?)
   - Review backup success/failure logs
   - Verify backup coverage (all critical data backed up?)
   - Check backup retention (90 days minimum recommended)

3. Ensure backup security:
   - Backups encrypted
   - Off-site or separate cloud region
   - Immutable (can't be encrypted by ransomware)
   - Access controlled (limited who can delete backups)

**Week 2: Test Restore**
1. Plan restore test (which system, when, how)
2. Perform restore test:
   - Restore database to non-production environment
   - Restore files from backup
   - Restore full system (if feasible)
3. Verify data integrity (data is complete and uncorrupted)
4. Document restore process and time (Recovery Time Objective - RTO)
5. Identify and fix any issues
6. Document restore test results

### Success Metrics

- **100% of critical systems** have backups running successfully
- **Backups tested quarterly** (or at least once before certification)
- **Restore successful** (data recovered completely)
- **RTO documented** (how long restore takes)
- **RPO acceptable** (how much data loss - e.g., last hour/day backup)

### Evidence for Audit

- Backup policy (frequency, retention, testing)
- Backup inventory (what's backed up)
- Backup success logs
- Restore test report (with screenshots, timing, results)
- Backup configuration (encryption, off-site, immutability)

---

## Quick Win #4: Deploy Endpoint Security

**Impact**: **HIGH** - Protects against malware, ransomware

**Effort**: 2-3 weeks

**Cost**: $3,000-$8,000 (endpoint security software + deployment)

### Why This Matters

- ISO 27001 Annex A.8.7 requires malware protection
- Endpoints (laptops, phones) are common attack entry points
- Ransomware, phishing, malware are prevalent threats
- Endpoint security provides detection and response

### Implementation Steps

**Week 1: Select Endpoint Security**
1. Choose endpoint security solution:
   - **Microsoft Defender** (included with Microsoft 365 E3/E5) - free if you have it
   - **CrowdStrike Falcon** - industry-leading EDR
   - **Carbon Black** - VMware EDR
   - **SentinelOne** - AI-powered EDR

2. Features needed:
   - Antivirus/anti-malware
   - Endpoint Detection and Response (EDR)
   - Encryption management (BitLocker, FileVault)
   - Patch management (optional, nice to have)
   - Remote wipe capability

**Week 2-3: Deploy**
1. Pilot with IT team
2. Configure policies (scan schedules, quarantine, alerts)
3. Roll out to all endpoints:
   - Laptops (company-issued)
   - Mobile devices (phones, tablets)
   - Desktops (if any)
4. Verify all devices enrolled
5. Enable encryption on all devices (BitLocker for Windows, FileVault for Mac)
6. Test detection (run safe malware test file - EICAR test file)

### Success Metrics

- **100% of endpoints protected** (all laptops, phones enrolled)
- **100% of devices encrypted** (full disk encryption)
- **Malware detections** (monitor and respond)
- **No unprotected devices** (regular scanning for unenrolled devices)

### Evidence for Audit

- Endpoint security policy
- Endpoint inventory (with protection status)
- Enrollment reports (100% coverage)
- Malware detection logs
- Encryption status reports
- Test results (EICAR detection)

---

## Quick Win #5: Security Awareness Training Kickoff

**Impact**: **HIGH** - Reduces human error, phishing success

**Effort**: 2-4 weeks (to launch; ongoing maintenance)

**Cost**: $3,000-$8,000 (training platform + content + launch)

### Why This Matters

- ISO 27001 Annex A.6.3 requires security awareness training
- Humans are the weakest link (phishing, social engineering)
- Training reduces phishing click rates by 50-70%
- Demonstrates security culture to auditors and clients

### Implementation Steps

**Week 1-2: Select Training Platform**
1. Choose platform:
   - **KnowBe4** - comprehensive security awareness and phishing
   - **Proofpoint Security Awareness** - integrated with email security
   - **SANS Security Awareness** - high-quality content
   - **Mimecast Awareness Training** - integrated platform
   - **Custom** - develop in-house (more effort, lower cost)

2. Content needed:
   - Security basics (passwords, MFA, phishing, malware)
   - Data handling (classification, protection, sharing)
   - Incident reporting (how to report, what to report)
   - Company policies (acceptable use, etc.)
   - Simulated phishing campaigns

**Week 3: Develop and Launch**
1. Customize training content (company branding, policies)
2. Communicate to all staff (why training matters, deadline)
3. Launch training (assign to all staff, 7-14 day deadline)
4. Track completion (daily reminders, escalation for non-compliance)
5. Run baseline phishing simulation

**Week 4: Report and Follow-Up**
1. Achieve 95%+ completion
2. Analyze results (test scores, weak areas)
3. Follow-up training for those who failed
4. Baseline phishing click rate (before training vs. after)
5. Report to management

### Success Metrics

- **95%+ completion rate** (within 30 days)
- **Phishing click rate <5%** (after training and simulations)
- **Improved security awareness** (measured by test scores, behavior change)

### Evidence for Audit

- Security awareness policy
- Training completion records (95%+ staff)
- Training content (slides, videos, tests)
- Phishing simulation results
- Ongoing training schedule (annual refresher)

---

## Quick Win #6: Data Classification Kickoff

**Impact**: **MEDIUM to HIGH** - Foundation for many controls

**Effort**: 2-3 weeks (to define and launch; ongoing to classify all data)

**Cost**: $2,000-$5,000 (policy, training, initial classification)

### Why This Matters

- ISO 27001 Annex A.5.12 requires data classification
- Can't protect data if you don't know what's sensitive
- Enables appropriate controls (encryption, access control, DLP)
- Many controls depend on data classification (e.g., "protect confidential data")

### Implementation Steps

**Week 1: Define Classification Scheme**
1. Create classification levels:
   - **PUBLIC**: No harm if disclosed (marketing materials, public website content)
   - **INTERNAL**: Minor harm if disclosed (internal memos, non-sensitive business data)
   - **CONFIDENTIAL**: Significant harm if disclosed (client data, business plans, contracts)
   - **RESTRICTED**: Severe harm if disclosed (personal data, financial data, trade secrets)

2. Define handling requirements for each level:
   - Access control (who can access)
   - Encryption (required for CONFIDENTIAL+)
   - Sharing (can share externally? requires approval?)
   - Storage (where can it be stored)
   - Deletion (retention and secure deletion)

3. Create data classification policy

**Week 2-3: Launch and Train**
1. Train staff on classification scheme (1 hour session)
2. Provide classification guidelines (flowchart, examples)
3. Classify key data assets:
   - Client databases (CONFIDENTIAL or RESTRICTED)
   - Data rooms (CONFIDENTIAL)
   - Financial data (RESTRICTED)
   - HR data (RESTRICTED for PII, INTERNAL for general)
   - Business plans (CONFIDENTIAL)
   - Marketing materials (PUBLIC)
4. Implement labeling (document headers/footers, email subject line tags)

### Success Metrics

- **Classification scheme defined and approved**
- **95%+ staff trained** on classification
- **Key data assets classified** (100% of high-value data)
- **Data handling controls aligned** with classification (encryption for CONFIDENTIAL+, etc.)

### Evidence for Audit

- Data classification policy
- Classification scheme (levels and handling requirements)
- Training records
- Classified data inventory
- Examples of labeled documents/emails
- Data handling procedures (aligned with classification)

---

## Quick Win #7: Privileged Access Management Basics

**Impact**: **HIGH** - Reduces risk of insider threats, credential misuse

**Effort**: 1-2 weeks

**Cost**: $2,000-$5,000 (mostly configuration and process)

### Why This Matters

- ISO 27001 Annex A.5.18 and A.8.2 require privileged access management
- Privileged accounts (admin, root) have excessive power
- Compromised privileged accounts = full system compromise
- Privileged access should be separate, monitored, and controlled

### Implementation Steps

**Week 1: Inventory and Separate**
1. Identify all privileged accounts:
   - Cloud admin (AWS root, Azure global admin, GCP project owner)
   - Server/system administrators
   - Database administrators
   - Application administrators
   - Security administrators

2. Separate privileged from standard accounts:
   - Every admin user should have 2 accounts:
     - Standard account (daily work, email, no admin rights)
     - Privileged account (admin tasks only, separate username)
   - Example: john.doe@company.com (standard), john.doe-admin@company.com (privileged)

3. Document privileged account inventory

**Week 2: Secure and Monitor**
1. Enforce MFA on all privileged accounts (mandatory, no exceptions)
2. Limit privileged account usage:
   - Use only for admin tasks
   - No email, no web browsing from privileged accounts
   - Log out when done
3. Implement monitoring:
   - Alert on privileged account usage
   - Log all privileged actions
   - Review privileged access quarterly
4. Create privileged access request process (for temporary admin access)

### Success Metrics

- **100% of privileged users have separate standard and privileged accounts**
- **100% of privileged accounts have MFA**
- **Privileged access monitored and logged**
- **Quarterly privileged access reviews**

### Evidence for Audit

- Privileged access management policy
- Privileged account inventory
- Separate account configurations
- MFA enforcement for privileged accounts
- Privileged access logs
- Quarterly review records

---

## Quick Win #8: Incident Reporting Mechanism

**Impact**: **MEDIUM** - Enables early incident detection and response

**Effort**: 1 week

**Cost**: $1,000-$2,000 (communication, process setup)

### Why This Matters

- ISO 27001 Annex A.6.8 requires incident reporting mechanism
- Early detection reduces incident impact
- Employees need easy way to report suspicious activity
- Encourages security culture (see something, say something)

### Implementation Steps

**Week 1: Setup and Communicate**
1. Create incident reporting channels:
   - Email: security@company.com (monitored by IT/ISMS Manager)
   - Phone/Slack: Optional, for urgent incidents
   - Web form: Optional, anonymous reporting

2. Define what to report:
   - Suspected phishing emails
   - Malware or virus detections
   - Lost or stolen devices
   - Unauthorized access attempts
   - Data breaches or leaks
   - Suspicious system behavior
   - Policy violations
   - Physical security concerns

3. Create incident reporting procedure (for employees):
   - What to report
   - How to report (email, phone, form)
   - What happens next (acknowledgment, investigation, feedback)

4. Communicate to all staff:
   - Email announcement
   - Include in security awareness training
   - Posters/reminders (physical and digital)
   - Emphasize no-blame culture (encourage reporting)

### Success Metrics

- **Incident reporting mechanism published and communicated to all staff**
- **Employees aware of how to report** (ask in training, measure awareness)
- **Incidents reported and tracked** (demonstrate process is working)
- **Feedback to reporters** (acknowledge and provide outcome)

### Evidence for Audit

- Incident reporting procedure
- Communication to staff (emails, training materials)
- Incident reports received (demonstrates process is used)
- Response and feedback records (shows process is working)

---

## Quick Win Summary: First 90 Days Plan

### Month 1 (Weeks 1-4): Foundation Quick Wins

**Week 1**:
- Enable MFA on all cloud services (start rollout)
- Enable audit logging on all systems

**Week 2**:
- Complete MFA rollout (100% enrollment)
- Verify backups are running

**Week 3**:
- Test backup restore
- Select endpoint security solution

**Week 4**:
- Deploy endpoint security (pilot with IT)
- Inventory privileged accounts

### Month 2 (Weeks 5-8): Protection Quick Wins

**Week 5-6**:
- Complete endpoint security rollout (100% devices)
- Separate privileged accounts
- Enable MFA on privileged accounts

**Week 7**:
- Define data classification scheme
- Create incident reporting mechanism

**Week 8**:
- Communicate data classification and incident reporting to staff
- Launch data classification training

### Month 3 (Weeks 9-12): Awareness Quick Wins

**Week 9-10**:
- Select security awareness training platform
- Customize training content

**Week 11**:
- Launch security awareness training (all staff)
- Classify key data assets

**Week 12**:
- Achieve 95%+ training completion
- Run baseline phishing simulation
- Report quick wins to management (metrics, achievements)

---

## Quick Wins ROI

| Quick Win | Cost | Risk Reduction | Time Savings (Incident Response) | Audit Value |
|-----------|------|----------------|--------------------------------|-------------|
| MFA | $2,000-$5,000 | 99% reduction in account compromise | ~$50,000 per prevented breach | Mandatory |
| Audit Logging | $500-$2,000 | Enables detection and investigation | ~20 hours per incident (faster investigation) | Mandatory |
| Backup Testing | $1,000-$3,000 | 90% reduction in data loss risk | ~$100,000+ per prevented data loss | Mandatory |
| Endpoint Security | $3,000-$8,000 | 80% reduction in malware incidents | ~$20,000 per prevented ransomware | Mandatory |
| Security Awareness | $3,000-$8,000 | 50-70% reduction in phishing success | ~$10,000 per prevented breach | Mandatory |
| Data Classification | $2,000-$5,000 | Enables appropriate controls | Foundation for many controls | Mandatory |
| Privileged Access Mgmt | $2,000-$5,000 | 70% reduction in insider threat risk | ~$50,000 per prevented insider incident | Mandatory |
| Incident Reporting | $1,000-$2,000 | Early detection (reduces impact 50%+) | ~10 hours per incident (faster response) | Mandatory |
| **TOTAL** | **$14,500-$38,000** | **Significant risk reduction** | **~$200,000+ in prevented losses** | **Foundation for ISO 27001** |

**Payback Period**: Immediate to 3 months (one prevented incident pays for all quick wins)

---

## Celebrating Quick Wins

**Week 12: Quick Wins Report to Management**

Create and present:
1. **Metrics Dashboard**:
   - MFA enrollment: 100%
   - Audit logging: 100% of systems
   - Backups tested: Success
   - Endpoint security: 100% devices protected
   - Training completion: 95%+
   - Phishing click rate: Baseline established
   - Data classification: Key assets classified
   - Incident reporting: Established and communicated

2. **Risk Reduction**:
   - Account compromise risk: 99% reduction
   - Malware risk: 80% reduction
   - Data loss risk: 90% reduction
   - Human error risk: 50-70% reduction

3. **Business Value**:
   - Estimated prevented losses: $200,000+
   - Foundation for ISO 27001: 8 critical controls implemented
   - Client confidence: Measurable security improvements
   - Audit readiness: Ahead of schedule

4. **Next Steps**:
   - Continue with Phase 1 (policies, risk assessment, vendor management)
   - Build on quick win momentum
   - Secure ongoing funding based on early results

---

**Recommendation**: Implement all 8 quick wins in the first 90 days. This delivers immediate risk reduction, builds stakeholder confidence, and creates strong foundation for ISO 27001 certification.
