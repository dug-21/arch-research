# ISO 27001 Implementation Roadmap - Prioritized 18-Month Plan

## Executive Summary

This roadmap provides a detailed, prioritized plan to achieve ISO 27001 certification in 18 months. The approach balances speed, cost-effectiveness, and risk reduction through three phases:

- **Phase 1 (Months 1-6)**: Foundation & Quick Wins - $35,000-$60,000
- **Phase 2 (Months 6-12)**: Core Controls Implementation - $40,000-$70,000
- **Phase 3 (Months 12-18)**: Optimization & Certification - $30,000-$45,000

**Total Investment**: $105,000-$175,000 over 18 months
**Ongoing Annual Cost**: $25,000-$45,000 post-certification

---

## Roadmap Principles

1. **Risk-Based**: Highest-risk areas addressed first
2. **Quick Wins**: Immediate value delivery (MFA, backups, logging)
3. **Leverage Cloud**: Inherit ~40% of controls from cloud providers
4. **Pragmatic**: "Fit for purpose" implementation, not perfection
5. **Phased**: Deliverables every 2-3 months to maintain momentum

---

## Phase 1: Foundation (Months 1-6)

**Goal**: Establish ISMS framework, conduct risk assessment, implement quick wins

**Budget**: $35,000-$60,000

**Key Deliverables**:
- ISMS foundation (scope, policies, risk assessment)
- Quick win controls (MFA, backups, logging, training)
- Asset and vendor inventories
- Initial policy framework

---

### Month 1: Program Launch & Quick Wins

**Week 1-2: Kickoff**
- [ ] Executive approval and budget authorization
- [ ] Appoint ISMS Manager/CISO
- [ ] Establish steering committee
- [ ] Select certification body (get 3 quotes)
- [ ] Procure policy templates or ISMS platform
- [ ] **Quick Win**: Enable MFA on all cloud services (AWS, Microsoft 365, Google Workspace)

**Week 3-4: ISMS Scope & Foundation**
- [ ] Define ISMS scope (what's in, what's out)
- [ ] Draft Information Security Policy
- [ ] Define roles and responsibilities (RACI matrix)
- [ ] **Quick Win**: Enable audit logging on all cloud services
- [ ] **Quick Win**: Verify backups are running, test restore

**Deliverables**:
- ISMS scope document
- Information Security Policy (draft for review)
- Roles and responsibilities matrix
- MFA enrollment report (target: 100%)
- Backup verification report

**Cost**: $8,000-$15,000 (consultant kickoff, templates, tools)

**Effort**: ISMS Manager (full-time), IT Manager (50%), Executive (10%)

---

### Month 2: Risk Assessment & Asset Inventory

**Week 1-2: Asset Inventory**
- [ ] Identify and document all information assets
- [ ] Cloud services inventory (AWS, Azure, SaaS apps)
- [ ] Data room inventory and classification
- [ ] Third-party/vendor inventory
- [ ] Assign asset owners
- [ ] Classify assets (confidentiality, integrity, availability)

**Week 3-4: Risk Assessment**
- [ ] Define risk assessment methodology
- [ ] Conduct risk assessment workshop (identify threats, vulnerabilities, impacts)
- [ ] Calculate risk levels
- [ ] **Quick Win**: Deploy endpoint security (antivirus/EDR) on all devices

**Deliverables**:
- Asset inventory (50-100+ assets)
- Risk assessment methodology document
- Risk register (20-50 identified risks)
- Risk assessment report
- Endpoint security deployment report

**Cost**: $10,000-$18,000 (risk assessment facilitation, endpoint security)

**Effort**: ISMS Manager (full-time), cross-functional team (20%)

---

### Month 3: Risk Treatment & Core Policies

**Week 1-2: Risk Treatment Planning**
- [ ] Prioritize risks (critical/high first)
- [ ] Select appropriate controls from Annex A
- [ ] Create risk treatment plan
- [ ] Identify controls to implement in each phase
- [ ] Create Statement of Applicability (SOA) - draft

**Week 3-4: Core Policies**
- [ ] Customize and approve core policies (5-6 policies):
  - Information Security Policy (finalize and approve)
  - Access Control Policy
  - Password and Authentication Policy
  - Data Classification and Handling Policy
  - Acceptable Use Policy
  - Incident Response Policy
- [ ] Executive approval of policies
- [ ] Communicate policies to all staff

**Deliverables**:
- Risk treatment plan
- Statement of Applicability (SOA) - draft
- 5-6 approved core policies
- Policy communication records

**Cost**: $6,000-$12,000 (policy customization, approvals)

**Effort**: ISMS Manager (full-time), Legal (review), Executive (approval)

---

### Month 4: Identity & Access Management

**Week 1-2: Identity Management**
- [ ] Implement centralized identity management (Azure AD, Okta, Google Workspace)
- [ ] Enforce MFA for all users (verify 100% enrollment)
- [ ] Define access control roles (RBAC)
- [ ] Create access request and approval process
- [ ] Document privileged accounts (separate from standard accounts)

**Week 3-4: Access Control Implementation**
- [ ] Implement RBAC in cloud services
- [ ] Configure access control matrix (who has access to what)
- [ ] Conduct initial access review (verify all access is appropriate)
- [ ] Implement privileged access management (separate admin accounts, MFA)
- [ ] **Quick Win**: Automated account deprovisioning on termination

**Deliverables**:
- Centralized identity management (100% users enrolled)
- MFA enforcement (100% users)
- RBAC role definitions
- Access control matrix
- Access request procedure
- Initial access review report

**Cost**: $8,000-$15,000 (identity platform, PAM, implementation)

**Effort**: IT Manager (80%), ISMS Manager (40%)

---

### Month 5: Data Classification & Protection

**Week 1-2: Data Classification**
- [ ] Define classification levels (Public, Internal, Confidential, Restricted)
- [ ] Create data classification policy and procedure
- [ ] Train staff on data classification
- [ ] Classify key data assets (client data, business data, data rooms)
- [ ] Implement data labeling (document headers, metadata tags)

**Week 3-4: Data Protection**
- [ ] Enable encryption at rest (cloud storage, databases)
- [ ] Verify encryption in transit (TLS 1.2+ for all services)
- [ ] Configure data room access controls and audit logging
- [ ] Implement clear desk/clear screen policy
- [ ] Deploy privacy screens for confidential work areas

**Deliverables**:
- Data classification scheme
- Data classification policy
- Training records (95%+ completion)
- Classified data inventory
- Encryption configurations (at rest and in transit)
- Data room access control matrix

**Cost**: $6,000-$12,000 (data classification, encryption, privacy screens)

**Effort**: ISMS Manager (60%), IT Manager (40%), All staff (training)

---

### Month 6: Training & Vendor Management

**Week 1-2: Security Awareness Training**
- [ ] Develop or procure security awareness training program
- [ ] Launch initial security awareness training (all staff, 1 hour)
- [ ] Onboarding security training (for new hires)
- [ ] Simulated phishing campaign (baseline)
- [ ] Track training completion (target: 95%+)

**Week 3-4: Third-Party/Vendor Management**
- [ ] Create third-party security policy
- [ ] Develop vendor security assessment questionnaire
- [ ] Inventory all third parties and cloud providers
- [ ] Collect compliance reports from cloud providers (ISO 27001, SOC 2)
- [ ] Assess high-risk vendors (those with access to sensitive data)
- [ ] Update contracts with security clauses (for new vendors)

**Deliverables**:
- Security awareness training program
- Training completion records (95%+ staff)
- Simulated phishing results (baseline)
- Third-party security policy
- Vendor inventory and risk assessments
- Cloud provider compliance reports (AWS, Azure, etc.)

**Cost**: $5,000-$10,000 (training platform, vendor assessments)

**Effort**: ISMS Manager (60%), HR (20%), Procurement (20%)

---

### Phase 1 Summary

**Timeline**: Months 1-6
**Budget**: $35,000-$60,000
**Team Effort**: ISMS Manager (1.0 FTE), IT Manager (0.5 FTE), Others (0.2 FTE)

**Key Achievements**:
- ISMS foundation established
- Risk assessment complete, treatment plan in place
- Quick wins delivered (MFA, backups, logging, endpoint security)
- Core policies approved and communicated
- Identity and access management implemented
- Data classification and protection
- Security awareness training launched
- Vendor management process

**Risk Reduction**: High - Addressed most critical security risks

---

## Phase 2: Core Controls Implementation (Months 6-12)

**Goal**: Implement remaining high and medium priority controls, enhance monitoring and response capabilities

**Budget**: $40,000-$70,000

---

### Month 7: Incident Response & Logging

**Week 1-2: Incident Response**
- [ ] Finalize incident response policy and plan
- [ ] Define incident response team (roles and responsibilities)
- [ ] Create incident classification scheme (P1/P2/P3/P4)
- [ ] Develop incident response playbooks (ransomware, phishing, data breach)
- [ ] Establish incident reporting mechanism (email, portal, phone)
- [ ] Train incident response team

**Week 3-4: Centralized Logging & Monitoring**
- [ ] Enable logging on all systems (cloud, applications, endpoints)
- [ ] Implement centralized log management (SIEM or cloud logging)
- [ ] Define log retention policy (1 year minimum)
- [ ] Configure log integrity protection (immutable logs)
- [ ] Set up basic monitoring alerts (failed logins, privileged access, config changes)

**Deliverables**:
- Incident response policy and plan
- Incident response playbooks (3-5 scenarios)
- Incident reporting procedure
- IR team training records
- Centralized logging implementation
- Log retention policy
- Basic monitoring alerts configured

**Cost**: $10,000-$18,000 (SIEM/logging tools, IR training)

**Effort**: IT Manager (80%), ISMS Manager (40%)

---

### Month 8: Network Security & Segmentation

**Week 1-2: Network Security**
- [ ] Implement network segmentation (prod, dev, management networks)
- [ ] Configure security groups and firewall rules (least privilege)
- [ ] Deploy WAF (Web Application Firewall) for web applications
- [ ] Implement VPN or zero-trust access for remote workers
- [ ] Review and harden cloud network configurations

**Week 3-4: Security Monitoring**
- [ ] Deploy cloud security monitoring (AWS GuardDuty, Azure Sentinel, GCP SCC)
- [ ] Configure security alerts (malware, unauthorized access, anomalies)
- [ ] Establish on-call rotation or monitoring schedule
- [ ] Test incident response (tabletop exercise)

**Deliverables**:
- Network segmentation architecture
- Security group configurations
- WAF deployment
- VPN/zero-trust access for remote workers
- Cloud security monitoring (GuardDuty, Sentinel, etc.)
- Security alerting rules
- Incident response tabletop exercise report

**Cost**: $12,000-$22,000 (network tools, WAF, security monitoring)

**Effort**: IT Manager (full-time), ISMS Manager (20%)

---

### Month 9: Vulnerability & Patch Management

**Week 1-2: Vulnerability Management**
- [ ] Implement vulnerability scanning (Nessus, Qualys, cloud-native)
- [ ] Conduct initial vulnerability scan (all systems)
- [ ] Prioritize vulnerabilities (critical/high/medium/low)
- [ ] Create vulnerability remediation process
- [ ] Set SLAs (critical: 7 days, high: 30 days, medium: 90 days)

**Week 3-4: Patch Management**
- [ ] Implement automated patching (OS, applications)
- [ ] Define patching schedule (monthly for non-critical, immediate for critical)
- [ ] Create patch testing process (test in dev/staging first)
- [ ] Track patch compliance (dashboard or reporting)
- [ ] Remediate critical and high vulnerabilities from initial scan

**Deliverables**:
- Vulnerability management policy and procedure
- Initial vulnerability scan report
- Vulnerability remediation tracking
- Automated patching configurations
- Patch compliance dashboard
- Remediation evidence (critical/high vulnerabilities)

**Cost**: $8,000-$15,000 (scanning tools, patching automation)

**Effort**: IT Manager (80%), ISMS Manager (20%)

---

### Month 10: Business Continuity & Disaster Recovery

**Week 1-2: Business Continuity Planning**
- [ ] Conduct business impact analysis (BIA)
- [ ] Define Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO)
- [ ] Create business continuity policy
- [ ] Develop business continuity procedures (for critical systems)
- [ ] Identify single points of failure
- [ ] Plan for continuity of security controls during disruption

**Week 3-4: Disaster Recovery**
- [ ] Design multi-region cloud deployment (or pilot light DR)
- [ ] Implement database replication (to secondary region)
- [ ] Configure automated failover (or documented manual failover)
- [ ] Test backup restore (full system restore test)
- [ ] Test DR failover process
- [ ] Document DR procedures

**Deliverables**:
- Business Impact Analysis (BIA)
- RTO/RPO definitions
- Business continuity policy and plan
- DR architecture (multi-region or pilot light)
- Database replication configuration
- Backup restore test report
- DR failover test report

**Cost**: $15,000-$30,000 (multi-region deployment, replication, testing)

**Effort**: IT Manager (full-time), ISMS Manager (30%)

---

### Month 11: Configuration & Change Management

**Week 1-2: Configuration Management**
- [ ] Define secure configuration baselines (CIS Benchmarks)
- [ ] Implement configuration management tools (Ansible, Terraform, cloud-native)
- [ ] Document current configurations
- [ ] Deploy configuration drift detection
- [ ] Remediate configuration drift
- [ ] Implement infrastructure as code (IaC) for cloud

**Week 3-4: Change Management**
- [ ] Create change management policy and procedure
- [ ] Implement change request and approval process
- [ ] Define change types (standard, normal, emergency)
- [ ] Establish Change Advisory Board (CAB) or approval authority
- [ ] Create change log and tracking
- [ ] Test change management process (pilot change)

**Deliverables**:
- Secure configuration baselines
- Configuration management implementation
- Configuration drift detection
- Infrastructure as code repository
- Change management policy and procedure
- Change request process and forms
- Change log

**Cost**: $8,000-$15,000 (configuration tools, change management system)

**Effort**: IT Manager (80%), ISMS Manager (40%)

---

### Month 12: Advanced Policies & Documentation

**Week 1-2: Complete Policy Set**
- [ ] Finalize remaining policies (total 10-15 policies):
  - Business Continuity Policy
  - Third-Party Security Policy (finalize)
  - Cloud Security Policy
  - Backup and Recovery Policy
  - Change Management Policy
  - Data Privacy Policy
  - Physical Security Policy
  - Remote Work Policy
  - Cryptography Policy
- [ ] Executive approval of all policies
- [ ] Communicate policy updates to staff
- [ ] Train staff on policy changes

**Week 3-4: Complete Procedure Set**
- [ ] Complete remaining procedures (total 15-20 procedures)
- [ ] Document all operational procedures
- [ ] Create process maps and flowcharts (optional but helpful)
- [ ] Implement document control procedure
- [ ] Organize all ISMS documentation

**Deliverables**:
- Complete policy set (10-15 policies, all approved)
- Complete procedure set (15-20 procedures)
- Policy communication records
- Training on policy updates
- Organized ISMS documentation repository

**Cost**: $5,000-$10,000 (policy finalization, documentation)

**Effort**: ISMS Manager (80%), Legal (review), All staff (training)

---

### Phase 2 Summary

**Timeline**: Months 6-12
**Budget**: $40,000-$70,000
**Team Effort**: IT Manager (0.8 FTE), ISMS Manager (0.6 FTE), Others (0.1 FTE)

**Key Achievements**:
- Incident response capability established
- Centralized logging and security monitoring
- Network security and segmentation
- Vulnerability and patch management operational
- Business continuity and disaster recovery tested
- Configuration and change management
- Complete policy and procedure set

**Risk Reduction**: Very High - Comprehensive control coverage

---

## Phase 3: Optimization & Certification (Months 12-18)

**Goal**: Prepare for and achieve ISO 27001 certification

**Budget**: $30,000-$45,000

---

### Month 13: Metrics & Continuous Improvement

**Week 1-2: ISMS Metrics**
- [ ] Define ISMS performance metrics (KPIs)
- [ ] Implement metrics collection (automated where possible)
- [ ] Create metrics dashboard
- [ ] Baseline current performance
- [ ] Define targets for improvement

**Week 3-4: Continuous Improvement**
- [ ] Review lessons learned from implementation
- [ ] Identify improvement opportunities
- [ ] Implement process improvements
- [ ] Optimize workflows (automation, simplification)
- [ ] Update documentation based on lessons learned

**Deliverables**:
- ISMS metrics and KPIs
- Metrics dashboard
- Baseline performance report
- Improvement initiatives log
- Updated procedures based on improvements

**Cost**: $4,000-$8,000 (metrics tools, improvement initiatives)

**Effort**: ISMS Manager (60%)

---

### Month 14: Internal Audit (Pre-Certification)

**Week 1: Audit Preparation**
- [ ] Develop internal audit program and schedule
- [ ] Select internal auditor (external consultant recommended for first audit)
- [ ] Define audit scope (cover all ISMS clauses and controls)
- [ ] Prepare audit evidence (collect and organize records)

**Week 2-3: Conduct Internal Audit**
- [ ] Opening meeting
- [ ] Document review (policies, procedures, mandatory documents)
- [ ] Interviews (ISMS Manager, IT Manager, staff sample)
- [ ] Evidence review (logs, records, configurations)
- [ ] Testing control effectiveness (sampling)
- [ ] Identify findings (nonconformities, observations)

**Week 4: Audit Reporting**
- [ ] Closing meeting
- [ ] Issue internal audit report
- [ ] Classify findings (major, minor, observations)
- [ ] Create corrective action plan
- [ ] Assign owners and deadlines for corrective actions

**Deliverables**:
- Internal audit program
- Internal audit plan
- Internal audit report
- Corrective action plan
- Evidence of audit (checklists, notes, interviews)

**Cost**: $8,000-$15,000 (external auditor for first internal audit)

**Effort**: ISMS Manager (full-time for audit), All staff (interviews)

---

### Month 15: Remediation & Management Review

**Week 1-3: Remediate Audit Findings**
- [ ] Implement corrective actions for all findings
- [ ] Document evidence of corrective actions
- [ ] Verify effectiveness (test that issue is resolved)
- [ ] Update documentation if processes changed
- [ ] Close corrective actions

**Week 4: Management Review**
- [ ] Prepare management review report (ISMS performance, audit results, metrics)
- [ ] Conduct management review meeting (CEO, ISMS Manager, key stakeholders)
- [ ] Present ISMS performance, risks, incidents, objectives progress
- [ ] Obtain management decisions (resource needs, objectives updates, improvements)
- [ ] Document management review results

**Deliverables**:
- Corrective action evidence (all findings closed)
- Effectiveness verification records
- Management review report
- Management review meeting minutes
- Management decisions and action items

**Cost**: $3,000-$6,000 (remediation effort, management reporting)

**Effort**: ISMS Manager (80%), IT Manager (40%), Executive (management review)

---

### Month 16: Stage 1 Certification Audit

**Week 1: Stage 1 Preparation**
- [ ] Finalize all ISMS documentation
- [ ] Ensure all mandatory documents are complete and approved
- [ ] Organize evidence for easy access
- [ ] Conduct final self-assessment (check all clauses and controls)
- [ ] Brief all staff on audit process

**Week 2-3: Stage 1 Audit (Documentation Review)**
- [ ] Certification body conducts Stage 1 audit
- [ ] Review ISMS documentation (scope, policy, risk assessment, SOA, procedures)
- [ ] Review organizational structure and roles
- [ ] Review competence records
- [ ] Verify readiness for Stage 2 audit
- [ ] Identify any documentation gaps or issues

**Week 4: Address Stage 1 Findings**
- [ ] Review Stage 1 audit report
- [ ] Address any findings or observations
- [ ] Update documentation if needed
- [ ] Prepare for Stage 2 audit (2-4 weeks later)

**Deliverables**:
- Complete ISMS documentation (audit-ready)
- Stage 1 audit report
- Evidence of addressing Stage 1 findings
- Readiness confirmation for Stage 2

**Cost**: $8,000-$12,000 (Stage 1 audit fees)

**Effort**: ISMS Manager (full-time), All staff (availability for audit)

---

### Month 17: Stage 2 Certification Audit

**Week 1: Stage 2 Preparation**
- [ ] Verify all controls are operational
- [ ] Collect latest evidence (logs, records, reports from past 3-6 months)
- [ ] Prepare for auditor interviews
- [ ] Conduct mock audit (internal team or consultant)
- [ ] Brief all staff on what to expect

**Week 2-3: Stage 2 Audit (Implementation Review)**
- [ ] Certification body conducts Stage 2 audit (on-site or virtual)
- [ ] Opening meeting
- [ ] Verify control implementation (sample evidence)
- [ ] Interviews with staff (verify understanding and compliance)
- [ ] Review records (access logs, incidents, training, backups, audits)
- [ ] Test control effectiveness (sample-based)
- [ ] Identify any nonconformities

**Week 4: Address Stage 2 Findings (if any)**
- [ ] Review Stage 2 audit report
- [ ] Implement corrective actions for any findings
- [ ] Provide evidence to certification body
- [ ] Certification body verifies corrective actions

**Deliverables**:
- Stage 2 audit evidence (6-12 months of records)
- Interview preparation
- Stage 2 audit report
- Corrective actions (if needed)
- Certification recommendation

**Cost**: $10,000-$15,000 (Stage 2 audit fees, corrective actions)

**Effort**: ISMS Manager (full-time), All staff (interviews, evidence)

---

### Month 18: Certification & Celebration

**Week 1-2: Certification Issuance**
- [ ] Certification body issues ISO 27001 certificate
- [ ] Receive certificate and logo usage guidelines
- [ ] Update website with ISO 27001 certification
- [ ] Notify clients and stakeholders

**Week 3-4: Post-Certification Activities**
- [ ] Celebrate with team (recognize contributions)
- [ ] Communicate achievement internally and externally
- [ ] Update marketing materials and proposals
- [ ] Plan for ongoing ISMS maintenance and surveillance audits
- [ ] Conduct project retrospective (lessons learned)

**Deliverables**:
- ISO 27001 Certificate
- Logo usage on website and materials
- Client notifications
- Surveillance audit schedule (annual)
- ISMS maintenance plan

**Cost**: $2,000-$4,000 (communications, celebration)

**Effort**: Marketing (communications), ISMS Manager (planning)

---

### Phase 3 Summary

**Timeline**: Months 12-18
**Budget**: $30,000-$45,000
**Team Effort**: ISMS Manager (0.8 FTE), IT Manager (0.3 FTE), All staff (audit participation)

**Key Achievements**:
- ISMS metrics and continuous improvement
- Internal audit conducted, findings remediated
- Management review completed
- Stage 1 and Stage 2 certification audits passed
- ISO 27001 CERTIFICATE ACHIEVED

---

## Post-Certification: Ongoing Maintenance

**Goal**: Maintain ISO 27001 certification through annual surveillance audits

**Annual Budget**: $25,000-$45,000

---

### Ongoing Activities (Annual)

**Quarterly**:
- [ ] Access reviews (verify access still appropriate)
- [ ] Metrics review and reporting
- [ ] Security awareness communications
- [ ] Vulnerability scans and remediation

**Semi-Annually**:
- [ ] Simulated phishing campaigns
- [ ] DR/BCP testing
- [ ] Management review (can be annual instead)

**Annually**:
- [ ] Security awareness training (all staff, refresher)
- [ ] Internal audit (full ISMS audit)
- [ ] Surveillance audit (certification body)
- [ ] Risk assessment (update for changes)
- [ ] Policy and procedure reviews (update as needed)
- [ ] Penetration testing (external)
- [ ] Vendor security assessments (high-risk vendors)

**As Needed**:
- [ ] Incident response (when incidents occur)
- [ ] Change management (for significant changes)
- [ ] Corrective actions (for audit findings or incidents)
- [ ] Training for new hires (onboarding)

---

### Annual Costs (Post-Certification)

| Activity | Cost |
|----------|------|
| Surveillance audit | $8,000-$12,000 |
| Internal audit (can be internal staff after Year 1) | $3,000-$6,000 |
| Security awareness training | $2,000-$4,000 |
| Penetration testing | $5,000-$10,000 |
| Vulnerability scanning | $2,000-$4,000 |
| ISMS platform subscription (if using) | $10,000-$20,000 |
| ISMS Manager / CISO (0.3-0.5 FTE ongoing) | $30,000-$50,000 |
| Continuous improvement initiatives | $5,000-$10,000 |
| **Subtotal (excluding FTE)** | **$25,000-$46,000** |
| **Total (including 0.4 FTE ISMS Manager)** | **$55,000-$96,000** |

**Note**: If you have dedicated ISMS Manager, ongoing maintenance is ~0.3-0.5 FTE (~40% of their time).

---

## Total Program Investment Summary

| Phase | Timeline | Budget | Cumulative |
|-------|----------|--------|------------|
| Phase 1: Foundation | Months 1-6 | $35,000-$60,000 | $35,000-$60,000 |
| Phase 2: Core Controls | Months 6-12 | $40,000-$70,000 | $75,000-$130,000 |
| Phase 3: Certification | Months 12-18 | $30,000-$45,000 | $105,000-$175,000 |
| **Total to Certification** | **18 months** | **$105,000-$175,000** | - |
| Annual Maintenance (ongoing) | Per year | $25,000-$45,000 | - |

---

## Critical Success Factors

1. **Executive Commitment**:
   - Secure CEO/Board sponsorship and budget
   - Regular steering committee meetings (monthly in Phase 1-2, quarterly thereafter)
   - Management review participation

2. **Dedicated Resources**:
   - ISMS Manager (0.5-1.0 FTE in Year 1, 0.3-0.5 FTE ongoing)
   - IT Manager support (0.3-0.8 FTE depending on phase)
   - Cross-functional participation (HR, Finance, Operations)

3. **Pragmatic Approach**:
   - "Fit for purpose" - don't over-engineer
   - Use templates and leverage cloud provider controls
   - Focus on value, not perfection

4. **Quick Wins**:
   - Deliver early value (MFA, backups, logging in Month 1-2)
   - Build momentum and stakeholder confidence
   - Use wins to secure ongoing funding

5. **Change Management**:
   - Communicate regularly (monthly updates to staff)
   - Train and engage employees (awareness, not just compliance)
   - Celebrate milestones (Phase completions, certification)

6. **Vendor Support**:
   - Engage consultant for guidance (not to do all the work)
   - Leverage ISMS platform for automation
   - Use certification body for readiness assessments

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| **Resource constraints** | Secure executive sponsorship early; consider consultant support |
| **Scope creep** | Define scope clearly in Month 1; resist changes mid-program |
| **Staff resistance** | Change management; training; communication; celebrate wins |
| **Budget overruns** | Detailed planning; track expenses; 15-20% contingency |
| **Audit failure** | Internal audit first (Month 14); address findings before certification audit |
| **Cloud provider changes** | Monitor provider compliance quarterly; have contingency for provider changes |
| **Timeline delays** | Buffer time (2-3 months); escalate blockers early; parallel work where possible |

---

## Alternative Timelines

### Accelerated (12 Months)

**Feasibility**: Possible with:
- Full-time dedicated ISMS Manager
- Higher consultant support (more expensive)
- Limited customization (heavy use of templates)
- Strong executive support and priority

**Budget**: $130,000-$200,000 (higher due to consultant costs)

**Risk**: Higher risk of audit failure; less time for organizational adoption

---

### Extended (24 Months)

**Feasibility**: Appropriate if:
- Limited internal resources (part-time ISMS Manager)
- Budget constraints (spread costs over longer period)
- Lower priority (other strategic initiatives taking precedence)

**Budget**: $90,000-$160,000 (lower annual spend, same total)

**Risk**: Loss of momentum; scope creep; longer time to business value

---

## Recommended: 18-Month Plan

**Best balance of**:
- Time to value (certification within 18 months)
- Cost efficiency (spread investment, leverage tools)
- Risk management (time for proper implementation and testing)
- Organizational adoption (sufficient time for change management)

---

## Next Steps (First 30 Days)

1. **Executive Approval** (Week 1):
   - Present roadmap and business case to CEO/Board
   - Secure budget approval
   - Identify ISMS Manager

2. **Vendor Selection** (Week 2):
   - Request proposals from 3-4 consultants (optional but recommended)
   - Request proposals from 3-4 certification bodies
   - Evaluate ISMS platforms (Vanta, Drata, Secureframe)

3. **Program Kickoff** (Week 3):
   - Establish steering committee
   - Select consultant (if using) and certification body
   - Procure ISMS platform or templates
   - Communicate program launch to all staff

4. **Quick Wins** (Week 4):
   - Enable MFA on all cloud services (100% enrollment)
   - Enable audit logging
   - Verify backups
   - Begin ISMS scope definition

**By End of Month 1**: MFA deployed, logging enabled, backups verified, scope defined, program underway

---

For detailed phase guides:
- [Phase 1: Foundation](phase-1-foundation.md)
- [Phase 2: Core Controls](phase-2-core-controls.md)
- [Phase 3: Optimization & Audit Prep](phase-3-optimization.md)
- [Quick Wins Guide](quick-wins.md)
