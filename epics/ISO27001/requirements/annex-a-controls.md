# ISO 27001:2022 Annex A Controls - Complete Guide

## Overview

Annex A contains 93 security controls organized into 4 domains. Your organization selects which controls to implement based on your risk assessment results. This guide provides practical implementation guidance for each control, tailored to your B2B

 cloud-based business.

**Key Principle**: You don't need to implement all 93 controls. Your risk assessment determines which controls are necessary, not necessary, or not applicable. The Statement of Applicability (SOA) documents your decisions.

**Four Domains**:
1. **Organizational Controls** (37 controls) - Policies, governance, people
2. **People Controls** (8 controls) - HR security, training, awareness
3. **Physical Controls** (14 controls) - Physical security, environmental
4. **Technological Controls** (34 controls) - Technical security measures

---

## How to Use This Document

For each control, you'll find:
- **Control objective**: What the control aims to achieve
- **Your implementation**: Practical approach for your organization
- **Cloud leverage**: How to inherit from cloud providers
- **Priority**: Critical/High/Medium/Low for your context
- **Cost estimate**: Implementation cost range
- **Evidence needed**: What auditors will look for

---

## Domain 1: Organizational Controls (37 Controls)

### A.5: Information Security Policies

#### A.5.1 Policies for Information Security

**Objective**: Provide management direction and support for information security.

**Your Implementation**:
- Create Information Security Policy (top-level, executive-approved)
- Develop 10-15 topic-specific policies (see policy templates guide)
- Annual review and approval process
- Communicate to all staff

**Mandatory Policies**:
1. Information Security Policy (master)
2. Acceptable Use Policy
3. Access Control Policy
4. Data Classification and Handling
5. Incident Response Policy
6. Business Continuity Policy
7. Third-Party Security Policy
8. Cloud Security Policy
9. Data Privacy Policy
10. Password and Authentication Policy

**Cloud Leverage**: None (organizational control)

**Priority**: **CRITICAL** (mandatory requirement)

**Cost**: $3,000-$6,000 (templates + customization)

**Evidence**: Approved policies, communication records, policy review schedule

---

### A.5.2 Information Security Roles and Responsibilities

**Objective**: Define and allocate information security responsibilities.

**Your Implementation**:
- Create RACI matrix for ISMS processes
- Update job descriptions with security responsibilities
- Document in organizational chart
- Communicate to all staff

**Key Roles**:
- Executive Sponsor
- ISMS Manager / CISO
- IT Manager
- Data Room Administrators
- All employees (general responsibilities)

**Cloud Leverage**: None (organizational control)

**Priority**: **CRITICAL**

**Cost**: $2,000-$4,000

**Evidence**: RACI matrix, job descriptions, organizational chart, communications

---

### A.5.3 Segregation of Duties

**Objective**: Reduce opportunities for unauthorized or unintentional modification or misuse.

**Your Implementation**:
- Identify high-risk processes requiring segregation
- Separate duties where practical (e.g., who can approve vs. execute changes)
- Implement compensating controls where segregation not feasible (e.g., enhanced logging, management review)

**Examples**:
- Different person requests vs. approves privileged access
- Different person develops vs. deploys to production
- Different person conducts vs. approves internal audits

**Cloud Leverage**: Cloud provider IAM can enforce segregation

**Priority**: **HIGH** (especially for privileged access, changes)

**Cost**: $3,000-$6,000 (process design, tool configuration)

**Evidence**: Process documentation, access control matrix, approval records

---

### A.5.4 Management Responsibilities

**Objective**: Require management to ensure security applies to all employees and contractors.

**Your Implementation**:
- Include security responsibilities in performance reviews
- Managers accountable for team compliance
- Regular management reporting on security metrics

**Cloud Leverage**: None

**Priority**: **MEDIUM**

**Cost**: $1,000-$2,000 (process integration)

**Evidence**: Performance review templates, management reports

---

### A.5.5 Contact with Authorities

**Objective**: Maintain appropriate contacts with relevant authorities.

**Your Implementation**:
- Document law enforcement contacts (cybercrime units)
- Identify regulatory authorities (data protection authority)
- Establish communication protocols
- Know when to contact (e.g., data breach notification requirements)

**Authorities to Contact**:
- Law enforcement (FBI, local cyber units) - for criminal activity
- Data protection authority - for data breaches (GDPR: 72 hours)
- Industry regulators - if applicable
- CERT/CSIRT - for cybersecurity incidents

**Cloud Leverage**: None

**Priority**: **MEDIUM**

**Cost**: $1,000-$2,000 (documentation)

**Evidence**: Contact list, communication protocols, breach notification procedure

---

### A.5.6 Contact with Special Interest Groups

**Objective**: Maintain appropriate contacts with special interest groups and security forums.

**Your Implementation**:
- Join industry security groups (ISACA, (ISC)2, industry associations)
- Subscribe to threat intelligence feeds
- Participate in information sharing communities
- Monitor security advisories from cloud providers

**Resources**:
- Cloud provider security bulletins (AWS, Azure, GCP)
- CISA alerts (Cybersecurity and Infrastructure Security Agency)
- Industry-specific ISACs (Information Sharing and Analysis Centers)

**Cloud Leverage**: None

**Priority**: **LOW to MEDIUM**

**Cost**: $500-$2,000/year (memberships, subscriptions)

**Evidence**: Membership records, threat intelligence subscriptions

---

### A.5.7 Threat Intelligence

**Objective**: Collect and analyze information about threats.

**Your Implementation**:
- Subscribe to threat intelligence feeds
- Review cloud provider security advisories
- Monitor industry threat reports
- Share relevant intelligence with stakeholders

**Sources**:
- Cloud provider security centers (free)
- CISA alerts (free)
- Industry threat reports (Verizon DBIR, etc.) (free)
- Commercial threat intelligence (optional)

**Cloud Leverage**: Cloud providers provide threat intelligence

**Priority**: **MEDIUM**

**Cost**: $0-$5,000/year (free to paid feeds)

**Evidence**: Threat intelligence subscriptions, review records, action taken

---

### A.5.8 Information Security in Project Management

**Objective**: Integrate information security into project management.

**Your Implementation**:
- Add security requirements to project templates
- Security review gate in project lifecycle
- ISMS Manager reviews projects involving information systems
- Risk assessment for new projects

**Project Security Checklist**:
- [ ] Data classification performed
- [ ] Access control requirements defined
- [ ] Security requirements documented
- [ ] Privacy impact assessed
- [ ] Third-party security reviewed
- [ ] ISMS documentation updated

**Cloud Leverage**: None

**Priority**: **MEDIUM**

**Cost**: $2,000-$4,000 (process integration)

**Evidence**: Project templates, security review records

---

### A.5.9 Inventory of Information and Other Associated Assets

**Objective**: Identify organizational assets and define protection responsibilities.

**Your Implementation**:
- Create and maintain asset inventory
- Classify each asset (confidentiality, integrity, availability)
- Assign asset owners
- Update inventory quarterly or when changes occur

**Asset Categories**:
1. **Information assets**: Client databases, intellectual property, business data
2. **Software assets**: Applications, cloud services, operating systems
3. **Physical assets**: Servers (if any), networking equipment, employee devices
4. **Services**: Cloud services, SaaS applications, third-party services
5. **People**: Key personnel, specialized skills

**Asset Inventory Fields**:
- Asset ID, Name, Description
- Asset Type, Owner
- Classification (Confidential/Internal/Public)
- Location (cloud region, office, etc.)
- Dependencies
- Business criticality

**Cloud Leverage**: Cloud provider asset discovery tools (AWS Config, Azure Resource Graph)

**Priority**: **CRITICAL** (required for risk assessment)

**Cost**: $5,000-$10,000 (initial inventory)

**Evidence**: Asset inventory spreadsheet or CMDB, classification scheme, owner assignments

---

### A.5.10 Acceptable Use of Information and Other Associated Assets

**Objective**: Identify, document, and implement rules for acceptable use.

**Your Implementation**:
- Acceptable Use Policy (AUP)
- Covers email, internet, devices, cloud services, data
- All employees acknowledge policy
- Enforce through technical controls and monitoring

**Acceptable Use Policy Topics**:
- Prohibited activities (illegal, unauthorized access, malware)
- Personal use boundaries
- Data handling requirements
- Email and communication standards
- Software installation restrictions
- Mobile device usage
- Remote access requirements
- Social media guidelines

**Cloud Leverage**: None (organizational control)

**Priority**: **HIGH**

**Cost**: $2,000-$4,000 (policy development, training)

**Evidence**: AUP document, employee acknowledgments, monitoring logs

---

### A.5.11 Return of Assets

**Objective**: Ensure personnel return all organizational assets upon termination.

**Your Implementation**:
- Offboarding checklist including asset return
- HR coordinates with IT
- Revoke access to systems
- Recover devices, access cards, keys
- Delete data from personal devices (if BYOD)

**Offboarding Checklist**:
- [ ] Disable user accounts (same day as termination)
- [ ] Revoke cloud access (AWS, Azure, SaaS apps)
- [ ] Recover laptop, phone, access badge
- [ ] Delete/wipe BYOD devices
- [ ] Revoke VPN/remote access
- [ ] Remove from data room permissions
- [ ] Transfer asset ownership (data, projects)
- [ ] Exit interview (security reminders)

**Cloud Leverage**: Automated account deprovisioning (identity management)

**Priority**: **HIGH**

**Cost**: $2,000-$3,000 (process documentation)

**Evidence**: Offboarding checklist, records of assets returned

---

### A.5.12 Classification of Information

**Objective**: Ensure information receives appropriate level of protection.

**Your Implementation**:
- Define classification levels
- Create classification guidelines
- Label information appropriately
- Handle information based on classification

**Classification Scheme**:

| Level | Description | Examples | Handling |
|-------|-------------|----------|----------|
| **PUBLIC** | No harm if disclosed | Marketing materials, public website | No restrictions |
| **INTERNAL** | Minor harm if disclosed | Internal memos, non-sensitive business data | Internal use only, no external sharing |
| **CONFIDENTIAL** | Significant harm if disclosed | Client data, business plans, contracts | Encryption, access control, need-to-know |
| **RESTRICTED** | Severe harm if disclosed | Personal data, financial data, trade secrets | Strict access control, encryption, audit logging, executive approval |

**Implementation**:
- Document classification policy
- Train staff on classification
- Label documents (headers, footers, metadata)
- Configure technical controls based on labels (DLP, encryption)

**Cloud Leverage**: Cloud data classification tools (Azure Information Protection, AWS Macie)

**Priority**: **CRITICAL** (foundation for many controls)

**Cost**: $4,000-$8,000 (policy, training, technical implementation)

**Evidence**: Classification policy, labeled documents, training records

---

### A.5.13 Labelling of Information

**Objective**: Develop and implement appropriate set of labels for information.

**Your Implementation**:
- Label documents with classification (header/footer)
- Email subject line prefixes for classified emails
- Metadata tags in cloud storage
- Visual labels (color coding, watermarks)

**Labelling Methods**:
- **Documents**: Header/footer ("CONFIDENTIAL - Internal Use Only")
- **Email**: Subject prefix ("[CONFIDENTIAL]")
- **Files**: Metadata tags, filename conventions
- **Physical**: Stamps, colored paper, envelopes

**Cloud Leverage**: Cloud DLP and labeling tools

**Priority**: **HIGH**

**Cost**: $2,000-$4,000 (templates, training)

**Evidence**: Labeling standards, examples of labeled documents

---

### A.5.14 Information Transfer

**Objective**: Maintain security of information transferred within organization and with external parties.

**Your Implementation**:
- Encrypted data transfer (TLS/SSL, VPN)
- Secure file transfer (SFTP, encrypted email, secure file sharing)
- Data transfer agreements with third parties
- Monitor and log file transfers

**Transfer Methods**:
- **Email**: Encrypted email for confidential data
- **File sharing**: Secure cloud sharing (OneDrive, Google Drive with encryption)
- **APIs**: TLS 1.2+ for API communications
- **Physical**: Encrypted USB drives (if necessary)

**Cloud Leverage**: Cloud providers encrypt data in transit by default

**Priority**: **HIGH**

**Cost**: $3,000-$6,000 (encryption tools, procedures)

**Evidence**: Encryption configurations, transfer logs, data transfer agreements

---

### A.5.15 Access Control

**Objective**: Establish and document access control rules.

**Your Implementation**:
- Access Control Policy
- Least privilege principle
- Role-Based Access Control (RBAC)
- Regular access reviews
- Automated provisioning/deprovisioning

**Access Control Principles**:
1. **Least Privilege**: Minimum access needed for job function
2. **Need-to-Know**: Access only to information required
3. **Separation of Duties**: Prevent conflicts of interest
4. **Time-bound**: Temporary elevated access expires

**Cloud Leverage**: Cloud IAM (AWS IAM, Azure AD, GCP IAM)

**Priority**: **CRITICAL**

**Cost**: $10,000-$20,000 (RBAC implementation, access review process)

**Evidence**: Access control policy, access matrix, review records

---

### A.5.16 Identity Management

**Objective**: Manage full lifecycle of identities.

**Your Implementation**:
- Centralized identity management (Azure AD, Okta, etc.)
- Unique user IDs (no shared accounts)
- Identity lifecycle: Create, modify, disable, delete
- Integration with HR system (automated onboarding/offboarding)

**Identity Lifecycle**:
1. **Provisioning**: New hire -> create account with appropriate access
2. **Modification**: Role change -> adjust access
3. **Suspension**: Leave of absence -> disable account
4. **Termination**: Employment end -> disable same day, delete after retention
5. **Review**: Quarterly access reviews

**Cloud Leverage**: Cloud identity providers (Azure AD, Google Workspace, Okta)

**Priority**: **CRITICAL**

**Cost**: $5,000-$15,000 (identity platform, integration)

**Evidence**: Identity management procedure, account creation/deletion records

---

### A.5.17 Authentication Information

**Objective**: Ensure allocation and management of authentication information.

**Your Implementation**:
- Strong password policy
- Multi-Factor Authentication (MFA) mandatory
- Secure password storage (password managers encouraged)
- No default/shared passwords
- Secure distribution of initial credentials

**Password Policy**:
- Minimum 12 characters (14+ recommended)
- Complexity: uppercase, lowercase, numbers, symbols
- No reuse of last 10 passwords
- Change on compromise
- MFA required (reduces password risk)

**MFA Implementation**:
- Enforce MFA for all users (cloud services, VPN, data rooms)
- Authenticator apps preferred (Microsoft Authenticator, Google Authenticator)
- SMS as fallback (less secure but better than none)
- No MFA bypass for privileged accounts

**Cloud Leverage**: Cloud provider MFA (Azure MFA, AWS MFA)

**Priority**: **CRITICAL** (Quick Win - implement Month 1-2)

**Cost**: $2,000-$5,000 (implementation, user enrollment)

**Evidence**: Password policy, MFA enrollment reports, configuration screenshots

---

### A.5.18 Access Rights

**Objective**: Provision, review, modify, and remove access rights.

**Your Implementation**:
- Formal access request and approval process
- Manager approval for standard access
- ISMS Manager approval for privileged/sensitive access
- Quarterly access reviews (recertification)
- Automated deprovisioning on termination

**Access Request Process**:
1. User/manager submits access request
2. Appropriate approver reviews and approves
3. IT provisions access
4. Access logged and recorded
5. Quarterly review of all access

**Access Review**:
- Quarterly: Review all user access
- Managers certify team members' access is appropriate
- Remove access no longer needed
- Document review results

**Cloud Leverage**: Cloud IAM automation, access request workflows

**Priority**: **CRITICAL**

**Cost**: $8,000-$15,000 (workflow implementation, review process)

**Evidence**: Access request records, approval logs, quarterly review reports

---

### A.5.19 Information Security in Supplier Relationships

**Objective**: Ensure protection of organization's assets accessible by suppliers.

**Your Implementation**:
- Supplier security requirements in contracts
- Supplier risk assessment before engagement
- Ongoing monitoring of supplier security
- Include cloud providers, SaaS vendors, all third parties

**Supplier Security Requirements**:
1. Comply with your security policies
2. Protect your data (confidentiality, integrity, availability)
3. Report security incidents (within 24 hours)
4. Allow security audits or provide compliance reports (SOC 2, ISO 27001)
5. Secure data deletion upon contract termination
6. Subcontractor approval and management

**Cloud Leverage**: Accept cloud provider certifications (ISO 27001, SOC 2)

**Priority**: **HIGH**

**Cost**: $10,000-$20,000 (contract templates, assessment process)

**Evidence**: Contracts with security clauses, supplier assessments, compliance reports

---

### A.5.20 Addressing Information Security within Supplier Agreements

**Objective**: Establish and agree with each supplier on security requirements.

**Your Implementation**:
- Security appendix to supplier contracts
- Define security requirements specific to service
- Include right to audit
- Incident notification requirements
- Data protection obligations

**Contract Security Clauses**:
- Security and privacy requirements
- Data protection and GDPR compliance
- Incident notification (24-48 hours)
- Right to audit or review certifications
- Data location and sovereignty
- Subcontractor management
- Termination and data return/deletion
- Liability and indemnification

**Cloud Leverage**: Cloud provider standard agreements typically include these

**Priority**: **HIGH**

**Cost**: $5,000-$10,000 (legal review, contract negotiation)

**Evidence**: Executed contracts with security appendices

---

### A.5.21 Managing Information Security in the ICT Supply Chain

**Objective**: Establish processes to manage information security risks in ICT supply chain.

**Your Implementation**:
- Identify ICT supply chain (cloud providers, SaaS, infrastructure)
- Assess supply chain risks
- Implement controls (contractual, technical, monitoring)
- Monitor supply chain security posture

**ICT Supply Chain for Your Organization**:
- Cloud infrastructure providers (AWS, Azure, GCP)
- SaaS applications (Salesforce, Microsoft 365, etc.)
- Data room platforms
- Identity providers (Okta, Azure AD)
- Backup and DR services
- Security tools (SIEM, vulnerability scanning, etc.)

**Supply Chain Risk Assessment**:
- Criticality to business
- Data sensitivity handled
- Vendor security maturity (certifications, breach history)
- Vendor financial stability
- Geographic risks (data sovereignty)

**Cloud Leverage**: Cloud providers manage their own supply chains

**Priority**: **MEDIUM to HIGH**

**Cost**: $5,000-$10,000 (assessment, monitoring process)

**Evidence**: Supply chain inventory, risk assessments, monitoring reports

---

### A.5.22 Monitoring, Review, and Change Management of Supplier Services

**Objective**: Monitor, review, and manage changes in supplier information security practices.

**Your Implementation**:
- Annual supplier security reviews
- Monitor supplier security notifications
- Review compliance reports (SOC 2, ISO 27001) annually
- Change notification requirements in contracts
- Incident reporting and tracking

**Supplier Monitoring Activities**:
- Review annual compliance reports (SOC 2, ISO 27001)
- Monitor security bulletins and incident notifications
- Track supplier incidents and response
- Conduct periodic security assessments (questionnaires)
- Review SLA performance

**Cloud Leverage**: Cloud providers publish compliance reports regularly

**Priority**: **MEDIUM**

**Cost**: $3,000-$8,000/year (review time, tools)

**Evidence**: Supplier review records, compliance reports collected, incident tracking

---

### A.5.23 Information Security for Use of Cloud Services

**Objective**: Establish processes for acquisition, use, management, and exit from cloud services.

**Your Implementation**:
- Cloud security policy
- Cloud service approval process
- Shared responsibility model understanding
- Cloud security configuration standards
- Regular cloud security assessments

**Shared Responsibility Model**:
```
Cloud Provider Responsible For:
- Physical infrastructure security
- Hypervisor and network infrastructure
- Managed service security (for PaaS/SaaS)

Your Organization Responsible For:
- Identity and access management
- Data encryption and classification
- Application security
- Security configuration
- Monitoring and logging
- Incident response
```

**Cloud Security Requirements**:
- Data encryption at rest and in transit
- MFA enforcement
- Logging and monitoring enabled
- Backup and disaster recovery configured
- Security groups and network controls
- Compliance with standards (ISO 27001, SOC 2)

**Cloud Leverage**: This IS about cloud - use cloud-native security tools

**Priority**: **CRITICAL** (you're heavily cloud-based)

**Cost**: $10,000-$20,000 (policy, assessments, configuration)

**Evidence**: Cloud security policy, configuration standards, cloud security assessments

---

### A.5.24 Information Security Incident Management Planning and Preparation

**Objective**: Plan and prepare for information security incident management.

**Your Implementation**:
- Incident Response Policy and Plan
- Incident response team (roles and responsibilities)
- Incident classification scheme
- Communication plan
- Tools and resources
- Regular testing (tabletop exercises)

**Incident Response Plan Components**:
1. **Preparation**: Tools, training, procedures
2. **Detection**: Monitoring, alerts, reporting
3. **Analysis**: Triage, classification, investigation
4. **Containment**: Isolate, prevent spread
5. **Eradication**: Remove threat, patch vulnerabilities
6. **Recovery**: Restore systems, verify security
7. **Lessons Learned**: Post-incident review, improvements

**Incident Classification**:
- **P1 Critical**: Business-critical system down, active breach
- **P2 High**: Significant incident, limited business impact
- **P3 Medium**: Security event requiring investigation
- **P4 Low**: Minor security concern

**Cloud Leverage**: Cloud provider incident response resources

**Priority**: **CRITICAL**

**Cost**: $8,000-$15,000 (plan development, training, tools)

**Evidence**: Incident response plan, team roster, exercise records

---

### A.5.25 Assessment and Decision on Information Security Events

**Objective**: Assess information security events and decide whether they are incidents.

**Your Implementation**:
- Event vs. incident definitions
- Triage process
- Escalation criteria
- Decision-making authority

**Event vs. Incident**:
- **Event**: Observable occurrence (e.g., failed login, firewall block)
- **Incident**: Event that compromises security (e.g., successful breach, malware infection)

**Triage Process**:
1. Event detected (automated alert, user report)
2. Initial analysis (Is this real? What's the impact?)
3. Classification (P1/P2/P3/P4)
4. Decision: Incident or not?
5. If incident: Activate incident response
6. If not: Document and close

**Cloud Leverage**: Cloud SIEM tools help with event correlation

**Priority**: **HIGH**

**Cost**: $3,000-$6,000 (process, training)

**Evidence**: Event/incident definitions, triage procedures, decision records

---

### A.5.26 Response to Information Security Incidents

**Objective**: Respond to information security incidents.

**Your Implementation**:
- Execute incident response plan (A.5.24)
- Contain and eradicate threat
- Preserve evidence
- Communication (internal and external)
- Recovery and validation
- Continuous improvement

**Response Playbooks** (develop for common scenarios):
- Ransomware attack
- Phishing/account compromise
- Data breach
- DDoS attack
- Insider threat
- Cloud misconfig exposure

**Communication**:
- Internal: Management, affected users, IT team
- External: Clients (if their data affected), authorities (if required), vendors (if involved)
- Legal counsel (for data breaches, regulatory requirements)

**Cloud Leverage**: Cloud provider support and forensics tools

**Priority**: **CRITICAL**

**Cost**: $5,000-$10,000 (playbooks, training, tools)

**Evidence**: Incident records, response documentation, communication logs

---

### A.5.27 Learning from Information Security Incidents

**Objective**: Ensure knowledge from security incidents is used to strengthen security.

**Your Implementation**:
- Post-incident review (PIR) for all P1/P2 incidents
- Identify root causes and contributing factors
- Implement corrective actions
- Update playbooks and procedures
- Share lessons learned (anonymized if needed)
- Track trends and patterns

**Post-Incident Review**:
1. What happened? (timeline, facts)
2. What was the impact?
3. What worked well in response?
4. What could be improved?
5. Root cause analysis
6. Preventive actions
7. Follow-up and verification

**Cloud Leverage**: Cloud provider shares lessons from their incidents

**Priority**: **MEDIUM to HIGH**

**Cost**: $2,000-$4,000 (process, facilitation)

**Evidence**: PIR reports, corrective action tracking, updated procedures

---

### A.5.28 Collection of Evidence

**Objective**: Establish procedures for identification, collection, acquisition, and preservation of evidence.

**Your Implementation**:
- Evidence handling procedure
- Chain of custody documentation
- Forensic readiness (tools, training)
- Legal hold process
- Evidence storage and retention

**Evidence Types**:
- Log files (system, application, cloud)
- Disk images
- Memory dumps
- Network traffic captures
- Email and communications
- Physical evidence (if applicable)

**Chain of Custody**:
- Who collected evidence
- When collected
- How collected (tools, methods)
- Where stored
- Who accessed it
- Hash values (integrity verification)

**Cloud Leverage**: Cloud providers preserve logs if requested promptly

**Priority**: **MEDIUM**

**Cost**: $3,000-$6,000 (procedure, tools, training)

**Evidence**: Evidence handling procedure, chain of custody forms

---

### A.5.29 Information Security during Disruption

**Objective**: Plan to maintain information security during disruption.

**Your Implementation**:
- Identify critical information security controls
- Ensure controls function during business continuity scenarios
- Test security during DR exercises
- Alternative security arrangements if primary fails

**Critical Security Controls to Maintain**:
- Access control (authentication still required)
- Encryption (data remains protected)
- Logging (incident detection continues)
- Incident response (capability maintained)
- Backup integrity (verify backups include security)

**Scenarios to Consider**:
- Cloud provider outage -> Failover to secondary region
- Ransomware attack -> Recovery from clean backups
- Key personnel unavailable -> Backup staff trained
- Security tool failure -> Manual procedures or alternative tools

**Cloud Leverage**: Multi-region cloud deployment, cloud backup

**Priority**: **MEDIUM to HIGH**

**Cost**: $5,000-$10,000 (planning, testing)

**Evidence**: Business continuity plan (security section), DR test results

---

### A.5.30 ICT Readiness for Business Continuity

**Objective**: Ensure ICT availability during disruption.

**Your Implementation**:
- Identify critical ICT systems
- Define recovery objectives (RTO, RPO)
- Implement redundancy and failover
- Regular backup and testing
- Disaster recovery plan

**Key Metrics**:
- **RTO (Recovery Time Objective)**: How quickly must system be restored?
- **RPO (Recovery Point Objective)**: How much data loss is acceptable?

**Example**:
```
Client Data Rooms:
- RTO: 4 hours (restore within 4 hours)
- RPO: 1 hour (max 1 hour of data loss)
- Implementation: Real-time replication, automated failover
```

**Cloud Leverage**: Cloud high availability, multi-region deployment, automated backups

**Priority**: **HIGH**

**Cost**: $15,000-$30,000 (redundancy, failover, testing)

**Evidence**: BCP/DR plan, RTO/RPO definitions, test results, backup logs

---

### A.5.31 Legal, Statutory, Regulatory, and Contractual Requirements

**Objective**: Identify, document, and meet legal, regulatory, and contractual requirements.

**Your Implementation**:
- Inventory applicable requirements
- Assign responsibility for compliance
- Monitor changes in requirements
- Regular compliance reviews
- Legal counsel consultation

**Requirements to Consider**:
- **GDPR**: If processing EU personal data
- **CCPA**: If processing California resident data
- **SOX**: If publicly traded
- **HIPAA**: If handling health information
- **PCI DSS**: If processing payment cards
- **Industry regulations**: Financial, healthcare, etc.
- **Contractual**: Client security requirements

**Compliance Register**:
| Requirement | Applicability | Owner | Status | Review Date |
|-------------|--------------|-------|--------|-------------|
| GDPR | Yes (EU clients) | Legal/ISMS Mgr | Compliant | Annual |
| ISO 27001 | Yes (certification goal) | ISMS Mgr | In progress | N/A |

**Cloud Leverage**: Cloud providers offer compliance certifications

**Priority**: **HIGH**

**Cost**: $5,000-$15,000 (legal review, compliance assessment)

**Evidence**: Compliance register, legal assessments, compliance reports

---

### A.5.32 Intellectual Property Rights

**Objective**: Implement appropriate procedures to protect intellectual property rights.

**Your Implementation**:
- Identify intellectual property (IP): Software, data, business processes
- Protect IP (copyrights, trademarks, trade secrets, NDAs)
- License compliance (software licensing)
- Employee IP assignment agreements
- Respect third-party IP

**IP Protection**:
- Source code protection (access control, version control)
- Trade secret protection (confidentiality agreements)
- Software licensing compliance (track licenses, prevent piracy)
- Employee agreements (IP belongs to company)

**Cloud Leverage**: Cloud providers respect your IP rights

**Priority**: **MEDIUM**

**Cost**: $3,000-$8,000 (legal agreements, license management)

**Evidence**: IP inventory, NDAs, employee IP agreements, license compliance reports

---

### A.5.33 Protection of Records

**Objective**: Protect records from loss, destruction, falsification, unauthorized access, and unauthorized release.

**Your Implementation**:
- Identify records requiring protection
- Define retention periods
- Implement protection controls (encryption, access control, backup)
- Secure disposal after retention period
- Legal hold process

**Record Types**:
- **Business records**: Contracts, financial records, tax documents
- **ISMS records**: Audit reports, risk assessments, management reviews
- **HR records**: Employment contracts, training records
- **Legal records**: Litigation holds, regulatory filings
- **Technical records**: Configurations, change logs, incident records

**Retention Periods** (examples):
- Tax records: 7 years
- Employment records: 7 years after termination
- Audit records: 3 years
- Incident records: 3 years
- Contracts: Duration + 7 years

**Cloud Leverage**: Cloud storage with versioning, immutability, retention policies

**Priority**: **MEDIUM**

**Cost**: $3,000-$6,000 (retention policy, implementation)

**Evidence**: Records retention schedule, protected records, disposal logs

---

### A.5.34 Privacy and Protection of PII

**Objective**: Ensure privacy and protection of personally identifiable information (PII).

**Your Implementation**:
- Identify PII processed
- Implement GDPR/privacy law requirements
- Privacy policy
- Data minimization
- Consent management
- Data subject rights (access, deletion, portability)
- Privacy impact assessments

**PII Categories**:
- Client contact information
- Employee personal data
- Donor information (for non-profit clients)
- Any data identifying individuals

**GDPR Compliance** (if applicable):
- Lawful basis for processing
- Data protection by design and default
- Privacy notices
- Consent management
- Data subject rights (DSAR process)
- Data breach notification (72 hours to authority, ASAP to individuals)
- DPO appointment (if required)

**Cloud Leverage**: Cloud providers offer GDPR-compliant services

**Priority**: **HIGH** (if processing EU personal data)

**Cost**: $10,000-$25,000 (GDPR compliance program)

**Evidence**: Privacy policy, GDPR compliance documentation, DSAR process, DPIAs

---

### A.5.35 Independent Review of Information Security

**Objective**: Ensure independent review of information security management.

**Your Implementation**:
- Internal audit (A.5.35 and ISO 27001 Clause 9.2)
- External assessment (penetration testing, vulnerability assessment)
- Management review (Clause 9.3)
- Independent consultant reviews

**Independent Reviews**:
1. **Internal Audit**: At least annually, by independent auditor
2. **External Audit**: Certification body (for ISO 27001)
3. **Penetration Testing**: Annually or after major changes
4. **Vulnerability Scanning**: Monthly
5. **Management Review**: At least annually

**Independence Criteria**:
- Auditor not auditing their own work
- External auditors preferred for objectivity
- Report to top management, not auditee

**Cloud Leverage**: Cloud providers undergo independent audits (share results)

**Priority**: **HIGH**

**Cost**: $8,000-$20,000/year (audits, pen tests, assessments)

**Evidence**: Audit reports, pen test reports, management review records

---

### A.5.36 Compliance with Policies, Rules, and Standards for Information Security

**Objective**: Ensure compliance with security policies, rules, and standards.

**Your Implementation**:
- Regular compliance monitoring
- Automated compliance checking (where possible)
- Self-assessments
- Internal audits
- Corrective actions for non-compliance

**Compliance Monitoring**:
- Automated: Configuration scanning, policy enforcement (Cloud Security Posture Management)
- Manual: Audits, reviews, assessments
- Continuous: Real-time monitoring

**Cloud Leverage**: Cloud compliance tools (AWS Config, Azure Policy, GCP Security Command Center)

**Priority**: **MEDIUM**

**Cost**: $5,000-$10,000 (tools, process)

**Evidence**: Compliance monitoring reports, self-assessment results, audit findings

---

### A.5.37 Documented Operating Procedures

**Objective**: Document and maintain operating procedures for information processing facilities.

**Your Implementation**:
- Document key operational procedures
- Keep procedures up to date
- Make procedures accessible to those who need them
- Version control

**Key Procedures to Document**:
1. Incident Response
2. Business Continuity and Disaster Recovery
3. Backup and Restore
4. Access Management (provisioning, deprovisioning, reviews)
5. Change Management
6. Monitoring and Logging
7. Vulnerability Management
8. Data Classification and Handling
9. Third-Party Management
10. Internal Audit

**Procedure Documentation Standards**:
- Purpose, scope, responsibilities
- Step-by-step instructions
- Tools and resources needed
- Escalation paths
- Review and approval

**Cloud Leverage**: Cloud provider documentation as reference

**Priority**: **MEDIUM to HIGH**

**Cost**: $10,000-$20,000 (documentation development)

**Evidence**: Procedure library, version control records

---

## Domain 2: People Controls (8 Controls)

### A.6: People Controls

#### A.6.1 Screening

**Objective**: Ensure personnel are suitable and understand responsibilities before employment.

**Your Implementation**:
- Background checks for all employees
- Reference checks
- Employment verification
- Criminal background check (where legal and appropriate)
- Different levels based on role sensitivity

**Screening Levels**:
- **Standard**: All employees - reference checks, employment verification
- **Enhanced**: Privileged access roles - criminal background check, credit check (for financial access)
- **Minimal**: Contractors with limited access - reference checks

**Cloud Leverage**: None (organizational control)

**Priority**: **MEDIUM to HIGH**

**Cost**: $100-$500 per employee (background check costs)

**Evidence**: Background check policy, background check records (secure storage)

---

#### A.6.2 Terms and Conditions of Employment

**Objective**: Ensure employees and contractors understand security responsibilities.

**Your Implementation**:
- Security responsibilities in employment contracts
- Confidentiality/NDA agreements
- Acceptable use acknowledgment
- IP assignment agreements
- Termination clauses (asset return, confidentiality survives)

**Contract Security Clauses**:
- Confidentiality obligations
- Data protection responsibilities
- Acceptable use of systems
- Incident reporting requirements
- Consequences of non-compliance
- IP belongs to organization
- Post-termination obligations

**Cloud Leverage**: None

**Priority**: **HIGH**

**Cost**: $2,000-$5,000 (legal review, contract updates)

**Evidence**: Employment contracts, NDAs, acknowledgment records

---

#### A.6.3 Information Security Awareness, Education, and Training

**Objective**: Ensure personnel receive appropriate awareness, education, and training.

**Your Implementation**:
- Security awareness training (all staff, annually)
- Onboarding security training (new hires)
- Role-specific training (IT, ISMS Manager, data room admins)
- Specialized training (incident response, forensics)
- Ongoing communications (newsletters, tips, simulated phishing)

**Training Program**:
1. **Onboarding** (new hires, 1 hour):
   - ISMS overview
   - Information security policy
   - Acceptable use
   - How to report incidents
   - Password/MFA setup

2. **Annual Refresher** (all staff, 1 hour):
   - Threat landscape update
   - Phishing and social engineering
   - Data handling best practices
   - Incident examples
   - Policy updates

3. **Role-Specific** (as needed):
   - ISO 27001 training for ISMS Manager
   - Cloud security for IT staff
   - Data classification for data owners
   - Incident response for IR team

4. **Ongoing Awareness** (monthly):
   - Security tips (email, Slack)
   - Simulated phishing exercises
   - Incident alerts and lessons learned

**Metrics**:
- Training completion rate (target: 95%)
- Phishing click rate (target: <5%)
- Incident reporting rate (increasing = good awareness)

**Cloud Leverage**: Cloud provider training resources (free)

**Priority**: **CRITICAL** (required by ISO 27001 Clause 7.3)

**Cost**: $8,000-$12,000 setup; $2,000-$4,000/year ongoing

**Evidence**: Training materials, completion records, awareness metrics

---

#### A.6.4 Disciplinary Process

**Objective**: Establish formal disciplinary process for personnel violating security.

**Your Implementation**:
- Define security violations and consequences
- Progressive discipline (warning, suspension, termination)
- Document process
- Consistent enforcement
- Investigation before discipline

**Security Violations** (examples):
- Sharing passwords
- Unauthorized data access or disclosure
- Installing unauthorized software
- Bypassing security controls
- Failing to report incidents
- Violating acceptable use policy

**Disciplinary Actions**:
1. **Minor violation**: Verbal warning, training, monitoring
2. **Moderate violation**: Written warning, mandatory training, privilege restriction
3. **Serious violation**: Suspension, termination, legal action

**Process**:
1. Incident detected
2. Investigation (gather facts)
3. Determination (violation severity)
4. Discipline (appropriate action)
5. Documentation
6. Follow-up (verify compliance)

**Cloud Leverage**: None

**Priority**: **MEDIUM**

**Cost**: $2,000-$4,000 (policy, HR integration)

**Evidence**: Disciplinary policy, records of actions taken (confidential)

---

#### A.6.5 Responsibilities after Termination or Change of Employment

**Objective**: Ensure security responsibilities continue after termination or role change.

**Your Implementation**:
- Continued confidentiality obligations (post-termination)
- Non-compete/non-solicit agreements (if applicable)
- Exit interview (security reminders)
- Asset return (covered in A.5.11)
- Access revocation (covered in A.5.18)

**Post-Termination Obligations**:
- Confidentiality survives termination (indefinitely for trade secrets)
- No unauthorized disclosure of information
- No unauthorized access to systems
- Return/destroy all company data
- Cooperation with investigations (if needed)

**Exit Process**:
1. Exit interview
   - Remind of ongoing confidentiality obligations
   - Collect assets
   - Obtain forwarding address
2. Disable access (same day)
3. Monitor for unauthorized access attempts
4. Document completion

**Cloud Leverage**: None

**Priority**: **MEDIUM**

**Cost**: $1,000-$2,000 (process documentation)

**Evidence**: Exit interview records, post-termination agreements

---

#### A.6.6 Confidentiality or Non-Disclosure Agreements

**Objective**: Ensure confidentiality or non-disclosure requirements are defined and reviewed.

**Your Implementation**:
- NDAs for all employees, contractors, third parties
- Confidentiality clauses in employment contracts
- Mutual NDAs with partners/vendors
- Regular review and updates
- Enforceability (legal review)

**When to Use NDAs**:
- All employees (can be part of employment contract)
- Contractors and consultants
- Third-party vendors with access to confidential data
- Business partners
- Potential acquisition targets (M&A)

**NDA Elements**:
- Definition of confidential information
- Obligations of receiving party
- Exclusions (public information, independently developed)
- Term and survival
- Remedies for breach

**Cloud Leverage**: NDAs with cloud providers (standard in contracts)

**Priority**: **HIGH**

**Cost**: $3,000-$6,000 (legal review, templates)

**Evidence**: Executed NDAs, NDA template

---

#### A.6.7 Remote Working

**Objective**: Implement security for remote working.

**Your Implementation**:
- Remote work policy
- Secure remote access (VPN or zero-trust)
- Endpoint security (antivirus, encryption, patching)
- MFA enforcement
- Acceptable use (home network security)
- Physical security (screen privacy, secure storage)

**Remote Work Security Requirements**:
1. **Access**: VPN or cloud-based access with MFA
2. **Devices**: Company-issued or secured BYOD
3. **Network**: Secure home Wi-Fi (WPA3, strong password)
4. **Physical**: Privacy screens, lock devices, secure workspace
5. **Data**: No local storage of confidential data (cloud-based)
6. **Monitoring**: Endpoint detection and response (EDR)

**Remote Access Options**:
- **VPN**: Traditional, secure tunnel to corporate network
- **Zero Trust / Cloud**: Cloud-based access, no VPN needed (preferred for cloud architecture)

**Cloud Leverage**: Cloud-based remote access (no VPN needed if zero-trust)

**Priority**: **HIGH** (likely have remote workers)

**Cost**: $5,000-$15,000 (VPN/zero-trust, endpoint security, policy)

**Evidence**: Remote work policy, VPN/access logs, endpoint security reports

---

#### A.6.8 Information Security Event Reporting

**Objective**: Ensure timely reporting of observed or suspected security events.

**Your Implementation**:
- Clear reporting mechanism (email, hotline, incident form)
- Encourage reporting (no-blame culture)
- Easy-to-use reporting process
- Acknowledge and respond to reports
- Feedback to reporters (outcome, lessons learned)

**What to Report**:
- Suspected malware or virus
- Phishing emails or suspicious messages
- Unauthorized access attempts
- Lost or stolen devices
- Data breaches or leaks
- Unusual system behavior
- Security policy violations
- Physical security concerns

**Reporting Channels**:
- Email: security@company.com
- Phone: Security hotline (if 24/7 support)
- Web form: Internal incident reporting form
- Manager: Report to supervisor
- Anonymous: Optional anonymous reporting

**Response**:
- Acknowledge report (within 1 hour)
- Initial triage (within 4 hours)
- Feedback to reporter (within 24 hours or when resolved)

**Cloud Leverage**: None (organizational process)

**Priority**: **HIGH**

**Cost**: $2,000-$5,000 (reporting process, communications)

**Evidence**: Reporting procedure, communication to staff, incident reports received

---

## Domain 3: Physical Controls (14 Controls)

**Note for Your Organization**: Since you're primarily cloud-based, many physical controls are **inherited from cloud providers**. Focus on office physical security and leverage cloud provider certifications for data center controls.

### A.7: Physical Controls

#### A.7.1 Physical Security Perimeters

**Objective**: Define and use physical security perimeters to protect areas containing information and information processing facilities.

**Your Implementation**:
- **Cloud data centers**: INHERITED from cloud providers (AWS/Azure/GCP have perimeter security)
- **Office locations**: Basic perimeter security (locked doors, badge access if applicable)
- Document reliance on cloud provider physical security

**Cloud Provider Physical Security**:
- Perimeter fencing and barriers
- Security guards and monitoring
- Intrusion detection systems
- Multiple security layers
- Certified (ISO 27001, SOC 2)

**Your Office**:
- Locked entrance during off-hours
- Badge access (if multi-tenant building)
- Visitor sign-in
- Minimal physical infrastructure (mostly cloud)

**Cloud Leverage**: **FULL INHERITANCE** for cloud data centers

**Priority**: **LOW** (inherited from cloud)

**Cost**: $1,000-$3,000 (office physical security, documentation)

**Evidence**: Cloud provider compliance reports (SOC 2, ISO 27001), office security documentation

---

#### A.7.2 Physical Entry

**Objective**: Secure areas should be protected by appropriate entry controls.

**Your Implementation**:
- **Cloud data centers**: INHERITED from cloud providers
- **Office**: Badge access or key access, visitor escort
- **Sensitive areas**: Server room (if any) - restricted access

**Cloud Provider Entry Controls**:
- Multi-factor authentication for data center access
- Biometric access controls
- Mantrap entrances
- Security guards
- Video surveillance

**Your Office Entry Controls**:
- Locked doors (after hours)
- Badge access (if applicable)
- Visitor log and escort
- Delivery acceptance procedure

**Cloud Leverage**: **FULL INHERITANCE** for cloud

**Priority**: **LOW** (inherited from cloud)

**Cost**: $500-$2,000 (visitor log, procedures)

**Evidence**: Cloud provider reports, visitor logs, access control records

---

#### A.7.3 Securing Offices, Rooms, and Facilities

**Objective**: Design and apply physical security for offices, rooms, and facilities.

**Your Implementation**:
- **Cloud**: INHERITED
- **Office**: Basic security for office space
- **Work from home**: Physical security requirements in remote work policy

**Office Security**:
- Lockable doors/windows
- Alarm system (if standalone office)
- Clean desk policy (lock away confidential documents)
- Secure disposal (shredders for confidential paper)

**Home Office Security** (remote workers):
- Secure workspace (lockable room preferred)
- Privacy screens
- Visitors don't access company systems
- Secure device storage when not in use

**Cloud Leverage**: **FULL INHERITANCE** for cloud

**Priority**: **LOW**

**Cost**: $1,000-$3,000 (clean desk policy, shredders, procedures)

**Evidence**: Office security procedures, clean desk policy, remote work policy

---

#### A.7.4 Physical Security Monitoring

**Objective**: Premises should be continuously monitored for unauthorized physical access.

**Your Implementation**:
- **Cloud**: INHERITED (24/7 monitoring)
- **Office**: Alarm system, video surveillance (if applicable)
- Minimal physical monitoring needed (cloud-based operations)

**Cloud Provider Monitoring**:
- 24/7 video surveillance
- Security operations center
- Intrusion detection
- Environmental monitoring

**Your Office** (if needed):
- Alarm system (notify security company/police)
- Video cameras (entrances)
- After-hours monitoring

**Cloud Leverage**: **FULL INHERITANCE** for cloud

**Priority**: **LOW**

**Cost**: $2,000-$5,000 (alarm/camera if not already installed)

**Evidence**: Cloud provider reports, office monitoring records (if applicable)

---

#### A.7.5 Protecting against Physical and Environmental Threats

**Objective**: Protect against physical and environmental threats (fire, flood, earthquake, etc.).

**Your Implementation**:
- **Cloud**: INHERITED (cloud data centers have extensive environmental controls)
- **Office**: Basic fire safety, no critical infrastructure at risk
- **Risk assessment**: Minimal physical infrastructure to protect

**Cloud Provider Environmental Protection**:
- Fire suppression systems
- HVAC and temperature control
- Redundant power (UPS, generators)
- Flood protection
- Seismic design (for earthquake zones)

**Your Office**:
- Fire alarms and extinguishers (building standard)
- Emergency evacuation plan
- No critical equipment (cloud-based)

**Cloud Leverage**: **FULL INHERITANCE** for cloud

**Priority**: **LOW**

**Cost**: $500-$1,000 (documentation, basic fire safety)

**Evidence**: Cloud provider reports, office building safety certificates

---

#### A.7.6 Working in Secure Areas

**Objective**: Design and apply security for working in secure areas.

**Your Implementation**:
- **Define secure areas**: Data rooms (virtual, in cloud), any office areas with sensitive data
- **Access controls**: Authorized personnel only
- **Clean desk**: No confidential data left unsecured
- **Visitor escorts**: If visitors in secure areas

**Secure Area Definition**:
- Physical: Office areas where confidential documents are used
- Virtual: Cloud data rooms, production environments

**Security Measures**:
- Access restrictions
- Clean desk policy
- Screen privacy (privacy filters)
- Lock screens when away
- No photography/recording

**Cloud Leverage**: Cloud data rooms are inherently secure areas

**Priority**: **MEDIUM**

**Cost**: $1,000-$3,000 (policy, privacy screens)

**Evidence**: Secure area definitions, clean desk policy, access records

---

#### A.7.7 Clear Desk and Clear Screen

**Objective**: Establish clear desk and clear screen policies.

**Your Implementation**:
- **Clear desk**: Lock away confidential documents when not in use
- **Clear screen**: Lock workstation when away
- **Automatic screen lock**: 5-10 minutes of inactivity
- **Training**: Awareness of policy and reasons

**Clear Desk Policy**:
- Lock away confidential documents at end of day
- No confidential data left on desks, printers, or whiteboards
- Shred confidential paper waste
- Secure storage (locked drawers, cabinets)

**Clear Screen Policy**:
- Lock workstation (Windows+L, Command+Control+Q) when leaving desk
- Automatic screen lock after 10 minutes idle
- Privacy screens to prevent shoulder surfing
- No unattended logged-in sessions

**Cloud Leverage**: Cloud systems can enforce automatic screen lock

**Priority**: **MEDIUM to HIGH**

**Cost**: $2,000-$4,000 (privacy screens, policy, training)

**Evidence**: Clear desk/screen policy, automatic lock configurations, training records

---

#### A.7.8 Equipment Siting and Protection

**Objective**: Protect equipment from physical and environmental threats.

**Your Implementation**:
- **Cloud**: INHERITED (cloud providers manage equipment)
- **Office equipment**: Minimal (workstations, printers)
- **Protection**: Basic environmental (no food/drink near computers)

**Cloud Provider Equipment Protection**:
- Climate-controlled data centers
- Redundant power and cooling
- Physical security
- Equipment maintenance

**Your Office**:
- Power surge protectors
- Adequate ventilation for equipment
- No liquids near computers
- Cable management (trip hazards)

**Cloud Leverage**: **FULL INHERITANCE** for cloud infrastructure

**Priority**: **LOW**

**Cost**: $500-$1,000 (surge protectors, cable management)

**Evidence**: Cloud provider reports, office equipment protection procedures

---

#### A.7.9 Security of Assets Off-Premises

**Objective**: Protect off-premises assets.

**Your Implementation**:
- **Laptops**: Encryption, strong passwords, MFA, remote wipe capability
- **Mobile devices**: MDM (Mobile Device Management), encryption, remote wipe
- **Portable storage**: Encrypted USB drives (if used - discouraged)
- **Documents**: Minimal paper documents off-premises

**Off-Premises Asset Security**:
- Full disk encryption (BitLocker, FileVault)
- MFA for access
- Remote lock/wipe (MDM for mobile, cloud-based for laptops)
- Physical security (don't leave unattended)
- VPN for network access
- No local storage of confidential data (use cloud)

**Cloud Leverage**: Cloud-based access reduces need for local data storage

**Priority**: **HIGH** (remote workforce)

**Cost**: $5,000-$10,000 (encryption, MDM, remote wipe capability)

**Evidence**: Encryption configurations, MDM enrollment, remote work policy

---

#### A.7.10 Storage Media

**Objective**: Manage storage media throughout its lifecycle.

**Your Implementation**:
- **Digital media**: Hard drives, USB drives, backup tapes (if used)
- **Lifecycle**: Procurement, use, transport, disposal
- **Protection**: Encryption, access control, secure disposal
- **Inventory**: Track media with confidential data

**Storage Media Management**:
1. **Procurement**: Approved vendors, encryption-ready media
2. **Use**: Encrypt confidential data, access control, inventory
3. **Transport**: Encrypted media, secure courier, chain of custody
4. **Disposal**: Secure erasure or physical destruction

**Disposal Methods**:
- **Software erasure**: Overwrite with random data (NIST 800-88 guidelines)
- **Physical destruction**: Shred, degauss, incinerate (for highly sensitive)
- **Certificate of destruction**: From disposal vendor

**Cloud Leverage**: Cloud storage media managed by provider (cryptographic erasure on disposal)

**Priority**: **MEDIUM**

**Cost**: $2,000-$5,000 (policy, disposal service, tracking)

**Evidence**: Media inventory, disposal certificates, encryption records

---

#### A.7.11 Supporting Utilities

**Objective**: Protect information processing facilities from power failures and other disruptions.

**Your Implementation**:
- **Cloud**: INHERITED (cloud data centers have redundant power, cooling, network)
- **Office**: Basic UPS for critical office equipment (if any)
- **Reliance**: Document dependency on cloud provider utilities

**Cloud Provider Utilities**:
- Redundant power feeds
- UPS and battery backup
- Diesel generators
- Redundant HVAC
- Multiple network providers

**Your Office**:
- UPS for network equipment (if critical)
- Backup internet connection (optional)
- Most operations cloud-based (resilient to office power outage)

**Cloud Leverage**: **FULL INHERITANCE** for cloud

**Priority**: **LOW**

**Cost**: $1,000-$3,000 (UPS if needed, documentation)

**Evidence**: Cloud provider reports, office UPS (if applicable)

---

#### A.7.12 Cabling Security

**Objective**: Protect cables carrying data or supporting information services.

**Your Implementation**:
- **Cloud**: INHERITED (cloud data center cabling secured)
- **Office**: Basic cable management, no critical cables
- **Network**: Wireless preferred (less cabling), secure Wi-Fi

**Cloud Provider Cabling**:
- Physically protected conduits
- Redundant cabling
- Network segregation
- Electromagnetic shielding

**Your Office**:
- Cable management (organized, no trip hazards)
- Locked network closets (if applicable)
- Secure Wi-Fi (WPA3, strong password)

**Cloud Leverage**: **FULL INHERITANCE** for cloud

**Priority**: **LOW**

**Cost**: $500-$1,000 (cable management, documentation)

**Evidence**: Cloud provider reports, office network diagram

---

#### A.7.13 Equipment Maintenance

**Objective**: Ensure availability, integrity, and confidentiality during equipment maintenance.

**Your Implementation**:
- **Cloud**: INHERITED (cloud provider maintains infrastructure)
- **Office equipment**: Vendor maintenance for printers, network gear
- **Laptops**: User responsibility, IT support, encryption ensures data protection

**Equipment Maintenance**:
1. **Cloud infrastructure**: Cloud provider responsibility
2. **Office equipment**: Vendor maintenance contracts, log maintenance
3. **Endpoints (laptops)**: Automated patching, encryption protects data during repair
4. **Third-party maintenance**: Data sanitization before sending for repair, or on-site repair

**Maintenance Security**:
- Supervised maintenance (if third-party in office)
- Data sanitization before external repair
- Verify equipment integrity after maintenance
- Maintain logs of maintenance activities

**Cloud Leverage**: **FULL INHERITANCE** for cloud infrastructure

**Priority**: **LOW**

**Cost**: $1,000-$2,000 (procedures, vendor contracts)

**Evidence**: Cloud provider reports, maintenance logs, vendor contracts

---

#### A.7.14 Secure Disposal or Re-Use of Equipment

**Objective**: Ensure secure disposal or re-use of equipment containing storage media.

**Your Implementation**:
- **Data sanitization**: Securely erase all data before disposal or re-use
- **Physical destruction**: For highly sensitive data or damaged media
- **Certificate of destruction**: From disposal vendor
- **Inventory tracking**: Remove from asset inventory

**Disposal Process**:
1. **Identify equipment for disposal**: End-of-life, replacement, damaged
2. **Data sanitization**:
   - Software erasure (NIST 800-88 Clear or Purge)
   - Physical destruction (degauss, shred, incinerate)
3. **Verification**: Confirm data is irrecoverable
4. **Physical disposal**: Recycling or destruction vendor
5. **Certificate**: Obtain certificate of destruction
6. **Inventory update**: Remove from asset inventory

**Re-Use**:
- Sanitize data before re-assigning to another user
- Verify sanitization
- Re-image with clean OS

**Cloud Leverage**: Cloud provider handles infrastructure disposal (cryptographic erasure)

**Priority**: **MEDIUM to HIGH**

**Cost**: $2,000-$5,000/year (disposal services)

**Evidence**: Disposal procedures, certificates of destruction, sanitization records

---

## Domain 4: Technological Controls (34 Controls)

### A.8: Technological Controls

#### A.8.1 User Endpoint Devices

**Objective**: Protect information on user endpoint devices.

**Your Implementation**:
- Endpoint security software (antivirus, EDR)
- Full disk encryption
- Automatic screen lock
- Automatic patching
- Remote wipe capability
- Acceptable use policy

**Endpoint Protection**:
- **Antivirus/EDR**: Microsoft Defender, CrowdStrike, Carbon Black
- **Encryption**: BitLocker (Windows), FileVault (Mac)
- **Patch management**: Automatic OS and app updates
- **Configuration**: Hardened security settings
- **Remote wipe**: MDM or cloud-based remote wipe

**Endpoint Types**:
- Laptops (company-issued)
- Mobile devices (phones, tablets)
- Desktops (if any)
- BYOD (if allowed - stricter controls)

**Cloud Leverage**: Cloud-based endpoint management (Microsoft Intune, Jamf, etc.)

**Priority**: **CRITICAL**

**Cost**: $10,000-$20,000 (endpoint security software, MDM, configuration)

**Evidence**: Endpoint security configurations, enrollment records, patch compliance reports

---

#### A.8.2 Privileged Access Rights

**Objective**: Allocate and manage privileged access rights.

**Your Implementation**:
- Identify privileged accounts (admin, root, cloud admin)
- Separate privileged accounts from standard user accounts
- MFA for privileged access (mandatory)
- Privileged access review (quarterly)
- Just-in-time (JIT) access (cloud-based)
- Privileged session monitoring and recording

**Privileged Access Types**:
- Cloud admin (AWS root, Azure global admin)
- Server/system admin
- Database admin
- Application admin
- Security admin

**Privileged Access Management (PAM)**:
- Separate accounts for privileged access (no daily use)
- MFA required for privileged access
- Time-limited access (JIT - request, approve, expire)
- Session recording (audit privileged actions)
- Regular review (who has privileged access, still needed?)

**Cloud Leverage**: Cloud PAM tools (AWS IAM, Azure AD PIM, GCP IAM)

**Priority**: **CRITICAL**

**Cost**: $8,000-$15,000 (PAM implementation, monitoring)

**Evidence**: Privileged account inventory, access reviews, session logs, MFA configurations

---

#### A.8.3 Information Access Restriction

**Objective**: Restrict access to information and application system functions.

**Your Implementation**:
- Access control based on business need-to-know
- RBAC (Role-Based Access Control)
- Data classification drives access
- Principle of least privilege
- Regular access reviews

**Access Control Model**:
```
User Role -> Permissions -> Information/Systems

Example:
- Sales Rep -> Read/Write Client Contact Info -> CRM
- Finance -> Read/Write Financial Data -> Accounting System
- Support -> Read-Only Client Data -> Support Portal
- Admin -> Full Access -> All Systems (privileged account)
```

**Access Restriction Mechanisms**:
- Authentication (who you are)
- Authorization (what you can access)
- Application-level controls (features available to role)
- Data-level controls (which records you can see)
- Network controls (which systems you can reach)

**Cloud Leverage**: Cloud IAM, cloud application RBAC

**Priority**: **CRITICAL**

**Cost**: $10,000-$20,000 (RBAC design and implementation)

**Evidence**: Access control matrix, role definitions, access review records

---

#### A.8.4 Access to Source Code

**Objective**: Manage and restrict access to source code.

**Your Implementation** (if you have software development):
- Source code repository access control (GitHub, GitLab, Bitbucket)
- Role-based access (developers, reviewers, release managers)
- No production code on developer workstations (use version control)
- Code review process
- Audit logs of code access and changes

**If No Software Development**:
- Document as "Not Applicable" in Statement of Applicability
- Still apply to configuration-as-code (infrastructure as code, cloud configs)

**Source Code Access Controls**:
- Developers: Read/Write access to repositories
- Reviewers: Approve pull requests
- Release managers: Deploy to production
- Segregation: Different permissions for dev, staging, production

**Cloud Leverage**: Cloud source code repositories (GitHub, GitLab, AWS CodeCommit)

**Priority**: **MEDIUM to HIGH** (if you develop software)

**Cost**: $3,000-$8,000 (repository access control, procedures)

**Evidence**: Repository access logs, code review records, access control policies

---

#### A.8.5 Secure Authentication

**Objective**: Implement secure authentication.

**Your Implementation**:
- MFA for all users (mandatory)
- Strong password policy
- Password managers (encouraged)
- SSO (Single Sign-On) for cloud services
- Biometric authentication (where available)

**Authentication Factors**:
1. **Something you know**: Password, PIN
2. **Something you have**: Phone (authenticator app), hardware token
3. **Something you are**: Fingerprint, face recognition

**MFA = at least 2 factors**

**Authentication Best Practices**:
- MFA mandatory for all users
- Passwordless preferred (Windows Hello, Face ID, hardware keys)
- SSO reduces password fatigue
- Adaptive authentication (risk-based MFA challenges)
- No SMS MFA for high-risk accounts (use authenticator apps or hardware tokens)

**Cloud Leverage**: Cloud identity providers (Azure AD, Okta, Google Workspace)

**Priority**: **CRITICAL** (Quick Win)

**Cost**: $3,000-$8,000 (MFA implementation, SSO configuration)

**Evidence**: MFA enrollment reports, authentication logs, password policy

---

#### A.8.6 Capacity Management

**Objective**: Monitor and project capacity to ensure required system performance.

**Your Implementation**:
- **Cloud-based**: Elastic scaling, cloud provider handles much of this
- Monitor resource utilization (CPU, memory, storage, network)
- Plan for growth
- Alerting on capacity thresholds
- Scale proactively before performance degrades

**Capacity Monitoring**:
- Cloud dashboards (AWS CloudWatch, Azure Monitor, GCP Stackdriver)
- Storage growth trends
- Database performance
- Application response times
- Network bandwidth

**Capacity Planning**:
- Annual capacity review
- Project growth based on business plans
- Budget for increased cloud usage
- Right-size cloud resources (cost optimization)

**Cloud Leverage**: **Cloud elastic scaling** (auto-scaling groups, serverless)

**Priority**: **MEDIUM**

**Cost**: $3,000-$8,000 (monitoring tools, capacity planning process)

**Evidence**: Capacity monitoring dashboards, capacity planning reports, auto-scaling configurations

---

#### A.8.7 Protection against Malware

**Objective**: Protect against malware.

**Your Implementation**:
- Endpoint antivirus/EDR (all devices)
- Cloud security tools (AWS GuardDuty, Azure Defender, GCP Security Command Center)
- Email filtering (anti-spam, anti-malware)
- Web filtering (block malicious sites)
- User awareness training (phishing, social engineering)
- Regular updates and patching

**Malware Protection Layers**:
1. **Endpoint**: Antivirus, EDR (Endpoint Detection and Response)
2. **Email**: Email gateway scanning (Microsoft Defender, Proofpoint, Mimecast)
3. **Web**: Web proxy/filtering (block malicious sites)
4. **Network**: Firewall, IDS/IPS (cloud-based)
5. **Cloud**: Cloud provider security tools
6. **User**: Training and awareness (don't click suspicious links)

**Malware Response**:
- Isolate infected device
- Scan and remediate
- Investigate spread
- Restore from clean backup if needed
- Lessons learned

**Cloud Leverage**: Cloud provider anti-malware tools (often included free)

**Priority**: **CRITICAL**

**Cost**: $8,000-$15,000 (endpoint security, email filtering)

**Evidence**: Antivirus configurations, malware detection logs, email filtering reports

---

#### A.8.8 Management of Technical Vulnerabilities

**Objective**: Prevent exploitation of technical vulnerabilities.

**Your Implementation**:
- Vulnerability scanning (monthly)
- Patch management process
- Critical patches within 7 days, high within 30 days
- Vulnerability remediation tracking
- Cloud security posture management

**Vulnerability Management Process**:
1. **Discover**: Vulnerability scanning (Nessus, Qualys, cloud-native tools)
2. **Assess**: Prioritize by severity and exploitability
3. **Remediate**: Patch, configure, mitigate
4. **Verify**: Re-scan to confirm remediation
5. **Report**: Track metrics, report to management

**Vulnerability Prioritization**:
- **Critical**: Actively exploited, public exploit available - patch within 7 days
- **High**: High severity, patch within 30 days
- **Medium**: Patch within 90 days
- **Low**: Patch during regular maintenance

**Cloud Leverage**: Cloud vulnerability scanning, patch management (AWS Systems Manager, Azure Update Management)

**Priority**: **CRITICAL**

**Cost**: $8,000-$15,000 (scanning tools, patch management)

**Evidence**: Vulnerability scan reports, patch compliance reports, remediation tracking

---

#### A.8.9 Configuration Management

**Objective**: Establish and maintain configurations.

**Your Implementation**:
- Document baseline configurations (hardened)
- Configuration management tools (Ansible, Terraform, cloud-native)
- Change control process
- Configuration drift detection
- Configuration as code (infrastructure as code)

**Configuration Management**:
1. **Baseline**: Define secure configurations (CIS Benchmarks)
2. **Implementation**: Apply configurations (automation)
3. **Monitoring**: Detect drift from baseline
4. **Remediation**: Restore compliant configuration
5. **Change Control**: Approve changes to baseline

**Configurations to Manage**:
- Operating systems (Windows, Linux, MacOS)
- Cloud infrastructure (VPCs, security groups, IAM)
- Applications (security settings)
- Network devices (firewalls, routers)

**Cloud Leverage**: Cloud configuration management (AWS Config, Azure Policy, GCP Config)

**Priority**: **HIGH**

**Cost**: $8,000-$15,000 (configuration management tools, baselines)

**Evidence**: Configuration baselines, configuration compliance reports, change records

---

#### A.8.10 Information Deletion

**Objective**: Delete information when no longer required.

**Your Implementation**:
- Data retention policy (how long to keep data)
- Automated deletion (where possible)
- Secure deletion (overwrite or cryptographic erasure)
- Legal hold process (suspend deletion for litigation)
- Deletion verification

**Data Retention**:
```
Data Type | Retention Period | Deletion Method
---------|------------------|----------------
Client data | Duration of contract + 7 years | Secure deletion
Financial records | 7 years | Secure deletion
HR records | 7 years after termination | Secure deletion
Backups | 90 days | Overwrite or cryptographic erasure
Logs | 1 year | Overwrite
Audit records | 3 years | Secure deletion
```

**Deletion Methods**:
- **Secure erasure**: Overwrite with random data (NIST 800-88)
- **Cryptographic erasure**: Destroy encryption key (for encrypted data)
- **Physical destruction**: Shred, degauss (for media disposal)

**Cloud Leverage**: Cloud data lifecycle policies (auto-delete after retention period)

**Priority**: **MEDIUM to HIGH** (GDPR requires timely deletion)

**Cost**: $3,000-$8,000 (retention policy, automated deletion)

**Evidence**: Data retention policy, deletion logs, verification records

---

#### A.8.11 Data Masking

**Objective**: Limit exposure of sensitive data through masking.

**Your Implementation**:
- Mask sensitive data in non-production environments (dev, test)
- Mask data in support scenarios (show only last 4 digits of SSN, credit card)
- Tokenization or pseudonymization for analytics
- Data minimization (collect only what's needed)

**Data Masking Techniques**:
- **Redaction**: Hide portions (e.g., ***** for passwords)
- **Substitution**: Replace with fake but realistic data
- **Shuffling**: Randomize data within column (preserve format)
- **Tokenization**: Replace with non-sensitive token, store mapping securely

**Use Cases**:
- Development/testing (use masked production data)
- Support and troubleshooting (support staff see masked data)
- Analytics (pseudonymize PII for analysis)
- Reporting (aggregate or mask individual data)

**Cloud Leverage**: Cloud data masking tools (AWS Macie, Azure SQL Data Masking)

**Priority**: **MEDIUM** (depends on data sensitivity)

**Cost**: $5,000-$12,000 (data masking tools, implementation)

**Evidence**: Data masking policy, masking configurations, non-production environment data samples

---

#### A.8.12 Data Leakage Prevention

**Objective**: Detect and prevent unauthorized disclosure of information.

**Your Implementation**:
- DLP (Data Leakage Prevention) tools
- Monitor and block sensitive data exfiltration
- Email DLP (scan outbound emails for sensitive data)
- Endpoint DLP (prevent copying to USB, unauthorized uploads)
- Cloud DLP (monitor cloud storage and apps)

**DLP Controls**:
1. **Discover**: Identify where sensitive data resides
2. **Monitor**: Track sensitive data movement
3. **Protect**: Block or alert on policy violations
4. **Respond**: Investigate and remediate incidents

**DLP Policies**:
- Block email containing credit card numbers to external recipients
- Alert when confidential documents uploaded to personal cloud storage
- Prevent copying sensitive data to USB drives
- Quarantine emails with PII sent externally without encryption

**Cloud Leverage**: Cloud DLP tools (Microsoft 365 DLP, Google Workspace DLP, cloud provider DLP)

**Priority**: **MEDIUM to HIGH** (depends on data sensitivity and risk)

**Cost**: $10,000-$25,000 (DLP tools, policies, monitoring)

**Evidence**: DLP policy configurations, DLP alerts and blocks, incident reports

---

#### A.8.13 Information Backup

**Objective**: Maintain copies of information and software to ensure availability.

**Your Implementation**:
- Automated backups (daily, hourly, or continuous)
- Cloud-based backup (AWS Backup, Azure Backup, cloud-native)
- Backup retention (90 days minimum, longer for compliance)
- Off-site and immutable backups (ransomware protection)
- Regular restore testing (quarterly)
- Backup monitoring and alerting

**Backup Strategy (3-2-1 Rule)**:
- **3** copies of data (production + 2 backups)
- **2** different media types (e.g., disk and cloud)
- **1** off-site copy

**Backup Scope**:
- Production databases (client data, business data)
- File storage (documents, data rooms)
- Cloud configurations (infrastructure as code)
- Application data (SaaS backups if not provider-managed)
- System configurations

**Backup Testing**:
- Quarterly restore tests
- Annual full disaster recovery test
- Document test results

**Cloud Leverage**: Cloud backup services (automated, off-site, immutable)

**Priority**: **CRITICAL** (Quick Win)

**Cost**: $5,000-$15,000 (backup storage, tools, testing)

**Evidence**: Backup policy, backup logs, restore test reports, backup monitoring

---

#### A.8.14 Redundancy of Information Processing Facilities

**Objective**: Implement redundancy to ensure availability.

**Your Implementation**:
- **Cloud multi-region**: Deploy critical systems in multiple cloud regions
- **Load balancing**: Distribute traffic across multiple instances
- **Database replication**: Real-time or near-real-time replication
- **Auto-scaling**: Automatically scale capacity based on demand
- **Failover**: Automatic or manual failover to secondary region

**Redundancy Strategies**:
1. **Active-Active**: Multiple regions serving traffic simultaneously
2. **Active-Passive**: Primary region serves traffic, standby ready to take over
3. **Pilot Light**: Minimal standby, scale up on failover
4. **Backup and Restore**: Restore from backup (slowest recovery)

**Your Implementation** (likely Active-Passive or Pilot Light):
- Primary cloud region for production
- Secondary region with standby infrastructure
- Database replication to secondary
- Automated or manual failover process
- Regular failover testing

**Cloud Leverage**: Cloud multi-region, auto-scaling, load balancing

**Priority**: **MEDIUM to HIGH** (depending on RTO/RPO requirements)

**Cost**: $15,000-$40,000 (multi-region deployment, replication, testing)

**Evidence**: Redundancy architecture, failover procedures, failover test results

---

#### A.8.15 Logging

**Objective**: Produce, store, protect, and analyze logs.

**Your Implementation**:
- Enable logging on all systems (cloud, applications, endpoints)
- Centralized log management (SIEM or cloud logging service)
- Log retention (1 year minimum, longer for compliance)
- Protect log integrity (immutable logs, hash verification)
- Monitor logs for security events

**Logs to Collect**:
- **Authentication**: Logins, logouts, failed attempts
- **Access**: File access, database queries, privileged commands
- **Changes**: Configuration changes, user/group changes, policy changes
- **Network**: Firewall logs, VPN connections, network flows
- **Security events**: Malware detections, vulnerability scans, incidents

**Log Management**:
1. **Collection**: Aggregate logs from all sources
2. **Storage**: Centralized, secure, retained per policy
3. **Analysis**: Monitor for security events, anomalies, compliance
4. **Alerting**: Real-time alerts on critical events
5. **Review**: Regular log review (automated and manual)

**Cloud Leverage**: Cloud logging services (AWS CloudTrail/CloudWatch, Azure Monitor, GCP Cloud Logging)

**Priority**: **CRITICAL**

**Cost**: $8,000-$20,000 (logging tools, storage, SIEM)

**Evidence**: Logging policy, log configurations, log retention, sample logs

---

#### A.8.16 Monitoring Activities

**Objective**: Monitor networks, systems, and applications for anomalous behavior.

**Your Implementation**:
- SIEM or cloud-native monitoring (AWS GuardDuty, Azure Sentinel, GCP Security Command Center)
- Real-time alerting on security events
- Baseline normal behavior, detect anomalies
- User behavior analytics (UBA) - detect insider threats
- 24/7 monitoring (or business hours with on-call)

**Monitoring Scope**:
- Failed login attempts (brute force, credential stuffing)
- Privileged access usage
- Unusual data access patterns
- Network anomalies (port scanning, unusual traffic)
- Configuration changes
- Malware and vulnerability exploitation attempts

**Monitoring Approach**:
1. **Automated**: SIEM, cloud security tools (real-time alerts)
2. **Manual**: Regular log review (weekly, monthly)
3. **On-call**: Respond to alerts 24/7 (or business hours)

**Cloud Leverage**: Cloud security monitoring (AWS GuardDuty, Azure Sentinel, GCP SCC)

**Priority**: **CRITICAL**

**Cost**: $10,000-$25,000 (SIEM or cloud monitoring, configuration, on-call)

**Evidence**: Monitoring configurations, alerting rules, monitoring reports, incident response records

---

#### A.8.17 Clock Synchronization

**Objective**: Synchronize clocks of systems for accurate timestamps.

**Your Implementation**:
- NTP (Network Time Protocol) configuration
- All systems sync to reliable time source
- Time zone consistency (UTC recommended for logs)
- Audit log timestamps for incident correlation

**Clock Synchronization**:
- **Cloud**: Automatically synced by cloud provider (NTP built-in)
- **Endpoints**: Sync to domain controller or NTP server
- **Applications**: Use system time (already synced)

**Importance**: Accurate timestamps critical for:
- Incident investigation (correlate events across systems)
- Audit compliance
- Legal evidence

**Cloud Leverage**: Cloud providers manage time sync automatically

**Priority**: **MEDIUM** (mostly automatic in cloud)

**Cost**: $500-$1,000 (verification, documentation)

**Evidence**: NTP configuration, time sync verification

---

#### A.8.18 Use of Privileged Utility Programs

**Objective**: Restrict and control use of privileged utility programs.

**Your Implementation**:
- Identify privileged utilities (system admin tools, database admin tools, cloud CLI)
- Restrict access to authorized personnel only
- MFA for privileged utility access
- Log and monitor usage
- Approval process for installation/use

**Privileged Utilities**:
- System admin tools (PowerShell, bash, system management consoles)
- Database admin tools (SQL clients, database management tools)
- Cloud admin tools (AWS CLI, Azure CLI, gcloud)
- Security tools (vulnerability scanners, penetration testing tools)
- Backup/restore tools

**Controls**:
- Access control (only privileged users)
- Logging (who used what, when)
- Monitoring (alert on privileged tool usage)
- Approval (manager approval for installation)
- Audit (review privileged tool usage quarterly)

**Cloud Leverage**: Cloud IAM restricts cloud CLI/API access

**Priority**: **MEDIUM to HIGH**

**Cost**: $3,000-$8,000 (access controls, logging, monitoring)

**Evidence**: Privileged utility inventory, access controls, usage logs

---

#### A.8.19 Installation of Software on Operational Systems

**Objective**: Implement procedures to control software installation.

**Your Implementation**:
- Whitelist-approved software
- Restrict installation rights (no local admin for standard users)
- Approval process for new software
- Vulnerability and malware scanning before installation
- Software inventory

**Software Installation Control**:
1. **Request**: User requests software (business justification)
2. **Approval**: Manager and IT approve
3. **Security review**: Scan for vulnerabilities, license compliance
4. **Install**: IT installs (or user if self-service approved list)
5. **Inventory**: Add to software inventory
6. **Monitor**: Detect unauthorized software installations

**Approved Software**:
- Standard business applications (Microsoft 365, Slack, Zoom, etc.)
- Approved development tools (if applicable)
- Security tools (antivirus, VPN)

**Unauthorized Software**:
- Personal software not related to business
- Unlicensed software (piracy)
- High-risk software (P2P, torrents)

**Cloud Leverage**: Cloud applications pre-approved, managed centrally

**Priority**: **MEDIUM to HIGH**

**Cost**: $5,000-$12,000 (software approval process, inventory tools, controls)

**Evidence**: Approved software list, installation approval records, software inventory

---

#### A.8.20 Network Security

**Objective**: Ensure security of networks and network services.

**Your Implementation**:
- Network segmentation (separate production, development, management)
- Firewall and security groups (cloud-based)
- Intrusion detection/prevention (IDS/IPS)
- VPN for remote access (or zero-trust cloud access)
- Network monitoring and logging
- Secure Wi-Fi (WPA3, strong password)

**Network Security Controls**:
1. **Perimeter**: Firewall, IDS/IPS (cloud security groups)
2. **Segmentation**: VLANs, subnets, separate environments
3. **Access control**: Who can access what network segments
4. **Encryption**: VPN, TLS for data in transit
5. **Monitoring**: Network traffic analysis, anomaly detection

**Cloud Network Security**:
- VPCs (Virtual Private Clouds) - isolated networks
- Security groups - firewall rules
- Network ACLs - additional network filtering
- VPN or Direct Connect - secure connectivity
- WAF (Web Application Firewall) - protect web apps

**Cloud Leverage**: Cloud network security services (AWS VPC, Azure VNet, GCP VPC)

**Priority**: **HIGH**

**Cost**: $8,000-$20,000 (network design, security groups, VPN, WAF)

**Evidence**: Network architecture, security group configurations, IDS/IPS logs, network monitoring

---

#### A.8.21 Security of Network Services

**Objective**: Ensure security features and service levels of network services.

**Your Implementation**:
- Define security requirements for network services
- SLAs with network service providers (ISP, cloud)
- Monitor network service performance and security
- Redundant network connections (if critical)

**Network Services**:
- Internet connectivity (ISP)
- Cloud connectivity (VPN, Direct Connect)
- DNS services
- CDN (Content Delivery Network)
- Email services
- VoIP services

**Security Requirements**:
- Availability SLA (e.g., 99.9% uptime)
- DDoS protection
- Encryption in transit
- Security monitoring and alerting
- Incident response from provider

**Cloud Leverage**: Cloud network services with built-in security and SLAs

**Priority**: **MEDIUM**

**Cost**: $3,000-$8,000 (SLA negotiation, monitoring)

**Evidence**: Network service agreements, SLA compliance reports, monitoring logs

---

#### A.8.22 Segregation of Networks

**Objective**: Segregate networks to separate information services, users, and systems.

**Your Implementation**:
- **Production vs. Non-Production**: Separate networks for production, development, testing
- **Internal vs. External**: Separate internal systems from internet-facing
- **Sensitive vs. General**: Separate networks for highly sensitive data
- **Cloud**: Use VPCs, subnets, security groups for segregation

**Network Segregation**:
```
Production VPC
  - Public Subnet (web servers, load balancers)
  - Private Subnet (application servers, databases)
  - Management Subnet (admin access, bastion hosts)

Development VPC (separate, no access to production data)

Corporate Network (office, remote workers)
```

**Segregation Controls**:
- Firewall rules between segments
- Least privilege network access
- No direct access from internet to internal systems (use bastion/jump hosts)
- Separate admin networks

**Cloud Leverage**: Cloud VPC segmentation, security groups

**Priority**: **HIGH**

**Cost**: $8,000-$15,000 (network design, implementation)

**Evidence**: Network architecture diagram, security group rules, network ACLs

---

#### A.8.23 Web Filtering

**Objective**: Manage access to external websites.

**Your Implementation**:
- Web proxy or cloud web filtering
- Block malicious and inappropriate websites
- Allow business-necessary sites
- Log web access for security monitoring
- User awareness (acceptable use)

**Web Filtering**:
- **Block**: Malware, phishing, adult content, illegal content
- **Monitor**: Social media, personal email (alert on excessive use)
- **Allow**: Business websites, cloud services, approved tools

**Web Filtering Tools**:
- Cloud web proxy (Zscaler, Cisco Umbrella)
- On-premise proxy (Squid, Microsoft Forefront TMG)
- DNS filtering (block malicious domains)
- Browser-based controls (enterprise browser policies)

**Cloud Leverage**: Cloud web filtering services

**Priority**: **MEDIUM**

**Cost**: $5,000-$12,000 (web filtering service, configuration)

**Evidence**: Web filtering policy, blocked site categories, web access logs

---

#### A.8.24 Use of Cryptography

**Objective**: Define and implement rules for effective use of cryptography.

**Your Implementation**:
- Cryptography policy (when to encrypt, what algorithms)
- Encryption for data at rest (databases, file storage, backups)
- Encryption for data in transit (TLS 1.2+, VPN)
- Key management (generation, storage, rotation, destruction)
- Use approved cryptographic algorithms (AES-256, RSA-2048+, SHA-256+)

**Cryptography Use Cases**:
1. **Data at Rest**:
   - Database encryption (TDE - Transparent Data Encryption)
   - File/object storage encryption (S3 encryption, Azure Storage encryption)
   - Disk encryption (BitLocker, FileVault)
   - Backup encryption

2. **Data in Transit**:
   - TLS/SSL for web, APIs, email
   - VPN for remote access
   - SFTP for file transfer

3. **Application-Level**:
   - Password hashing (bcrypt, PBKDF2, Argon2)
   - Application data encryption

**Key Management**:
- Use cloud key management (AWS KMS, Azure Key Vault, GCP KMS)
- Rotate keys annually or after compromise
- Separate keys for different environments (prod, dev, test)
- Destroy keys securely when no longer needed

**Cloud Leverage**: Cloud-managed encryption and key management

**Priority**: **CRITICAL**

**Cost**: $8,000-$20,000 (encryption implementation, key management)

**Evidence**: Cryptography policy, encryption configurations, key management procedures

---

#### A.8.25 Secure Development Life Cycle

**Objective**: Establish and apply rules for secure development.

**Your Implementation** (if you develop software):
- Secure development policy
- Security requirements in design phase
- Secure coding standards
- Code review (peer review, automated scanning)
- Security testing (SAST, DAST, penetration testing)
- Vulnerability remediation before release

**If No Software Development**:
- Document as "Not Applicable" in Statement of Applicability
- Apply secure configuration practices to cloud infrastructure and SaaS apps

**Secure Development Lifecycle (SDLC)**:
1. **Requirements**: Define security requirements
2. **Design**: Threat modeling, security architecture
3. **Development**: Secure coding, code review
4. **Testing**: Security testing (SAST, DAST, pen test)
5. **Deployment**: Secure configuration, release approval
6. **Maintenance**: Patch vulnerabilities, monitor for issues

**Cloud Leverage**: Cloud-native security testing tools

**Priority**: **MEDIUM to HIGH** (if you develop software); **LOW/N/A** if not

**Cost**: $10,000-$30,000 (if developing software - tools, training, process)

**Evidence**: Secure development policy, code review records, security test reports

---

#### A.8.26 Application Security Requirements

**Objective**: Identify, specify, and approve information security requirements.

**Your Implementation**:
- Security requirements for all applications (developed or procured)
- Authentication and authorization requirements
- Data protection requirements (encryption, classification)
- Logging and monitoring requirements
- Input validation and output encoding (prevent injection attacks)
- Secure session management

**Application Security Requirements**:
1. **Authentication**: MFA, strong passwords, SSO
2. **Authorization**: RBAC, least privilege
3. **Data Protection**: Encryption, data masking, DLP
4. **Input Validation**: Prevent SQL injection, XSS, command injection
5. **Session Management**: Secure cookies, timeout, logout
6. **Logging**: Audit logs, error logging (no sensitive data in logs)
7. **Error Handling**: Generic error messages (don't reveal system details)

**Cloud Leverage**: Cloud application security services (WAF, API Gateway)

**Priority**: **HIGH**

**Cost**: $8,000-$20,000 (security requirements definition, testing, implementation)

**Evidence**: Security requirements documents, security architecture, test results

---

#### A.8.27 Secure System Architecture and Engineering Principles

**Objective**: Apply principles for engineering secure systems.

**Your Implementation**:
- Security by design (build security in from the start)
- Defense in depth (multiple layers of security)
- Least privilege
- Separation of duties
- Fail secure (default deny)
- Simplicity (less complexity = fewer vulnerabilities)

**Secure Architecture Principles**:
1. **Defense in Depth**: Multiple security layers (firewall, WAF, app security, encryption)
2. **Least Privilege**: Minimum access necessary
3. **Separation of Duties**: Prevent conflicts of interest
4. **Fail Secure**: If security control fails, deny access (don't allow)
5. **Security by Default**: Secure configurations out of the box
6. **Minimize Attack Surface**: Disable unnecessary services, close unused ports
7. **Simplicity**: Simpler systems are more secure (fewer bugs, easier to audit)

**Your Cloud Architecture**:
- Multi-tier architecture (web, app, data layers separated)
- Security controls at each layer
- Least privilege IAM
- Network segmentation
- Encryption everywhere

**Cloud Leverage**: Cloud secure architecture best practices (AWS Well-Architected, Azure Architecture Center)

**Priority**: **HIGH**

**Cost**: $10,000-$25,000 (architecture design, security review)

**Evidence**: System architecture documents, security architecture review, design principles

---

#### A.8.28 Secure Coding

**Objective**: Apply secure coding principles in software development.

**Your Implementation** (if you develop software):
- Secure coding standards (OWASP, CERT)
- Training for developers (secure coding)
- Code review (peer and automated)
- Static analysis (SAST tools)
- Vulnerability remediation

**If No Software Development**:
- Document as "Not Applicable"
- Apply to infrastructure as code (Terraform, CloudFormation) - secure configurations

**Secure Coding Principles**:
1. **Input Validation**: Validate all inputs (whitelist, not blacklist)
2. **Output Encoding**: Encode outputs (prevent XSS)
3. **Parameterized Queries**: Prevent SQL injection
4. **Authentication/Authorization**: Enforce at every layer
5. **Error Handling**: Generic error messages, log details securely
6. **Cryptography**: Use proven libraries, don't roll your own crypto
7. **Secure Defaults**: Deny by default, explicit allow

**OWASP Top 10** (common vulnerabilities to avoid):
- Injection, Broken Authentication, Sensitive Data Exposure, XML External Entities (XXE), Broken Access Control, Security Misconfiguration, Cross-Site Scripting (XSS), Insecure Deserialization, Using Components with Known Vulnerabilities, Insufficient Logging & Monitoring

**Cloud Leverage**: Cloud secure coding resources, code scanning tools

**Priority**: **HIGH** (if developing software); **N/A** if not

**Cost**: $8,000-$20,000 (training, tools, code review)

**Evidence**: Secure coding standards, training records, code review reports, SAST scan results

---

#### A.8.29 Security Testing in Development and Acceptance

**Objective**: Define and implement security testing in development process.

**Your Implementation** (if you develop software):
- Security testing in CI/CD pipeline
- Static Application Security Testing (SAST) - code analysis
- Dynamic Application Security Testing (DAST) - runtime testing
- Dependency scanning (vulnerable libraries)
- Penetration testing before production release

**If No Software Development**:
- Apply to cloud infrastructure testing
- Vulnerability scanning of cloud configurations
- Penetration testing of cloud environment

**Security Testing Types**:
1. **SAST (Static)**: Analyze source code for vulnerabilities (SonarQube, Checkmarx)
2. **DAST (Dynamic)**: Test running application (OWASP ZAP, Burp Suite)
3. **IAST (Interactive)**: Combine SAST and DAST
4. **Dependency Scan**: Check for vulnerable libraries (Snyk, OWASP Dependency-Check)
5. **Penetration Test**: Simulate real attack (annual, by external expert)

**Testing Frequency**:
- SAST/Dependency scan: Every code commit (automated in CI/CD)
- DAST: Weekly or before releases
- Penetration test: Annually or before major releases

**Cloud Leverage**: Cloud security testing tools (AWS Inspector, Azure Security Center)

**Priority**: **HIGH** (if developing software or managing cloud infrastructure)

**Cost**: $10,000-$30,000 (testing tools, penetration tests)

**Evidence**: Security testing policy, test results, penetration test reports, vulnerability remediation records

---

#### A.8.30 Outsourced Development

**Objective**: Supervise and monitor outsourced system development.

**Your Implementation** (if you outsource development):
- Security requirements in contracts with developers
- Code review and security testing of outsourced code
- Source code escrow (ensure access if vendor fails)
- IP ownership clarification
- Vendor security vetting

**If No Outsourced Development**:
- Document as "Not Applicable"
- Apply to outsourced cloud services and SaaS (covered in supplier controls A.5.19-A.5.22)

**Outsourced Development Controls**:
- Security requirements defined upfront
- Secure development lifecycle required
- Code review (access to source code)
- Security testing (SAST, DAST, pen test)
- Vulnerability remediation SLA
- Code escrow agreement
- IP ownership in contract

**Cloud Leverage**: Apply to cloud infrastructure as code development

**Priority**: **MEDIUM** (if outsourcing development); **N/A** if not

**Cost**: $5,000-$15,000 (contract clauses, code review, security testing)

**Evidence**: Contracts with security requirements, code review records, security test results

---

#### A.8.31 Separation of Development, Test, and Production Environments

**Objective**: Separate development, testing, and production environments.

**Your Implementation**:
- Separate cloud accounts or VPCs for dev, test, prod
- No production data in dev/test (use masked or synthetic data)
- Different access controls (developers have access to dev, not prod)
- Separate credentials and keys
- Change management for production deployments

**Environment Separation**:
```
Development Environment:
- Developers have access
- Test/demo data
- Frequent changes
- Lower security standards (no PII)

Testing/Staging Environment:
- QA team has access
- Masked production data
- Pre-production testing
- Similar security to production

Production Environment:
- Limited access (operations, support)
- Real customer data
- Change control required
- Highest security standards
```

**Separation Controls**:
- Separate cloud accounts/VPCs
- Separate databases (no shared databases)
- Separate IAM roles and credentials
- Separate encryption keys
- Firewall rules prevent dev access to prod

**Cloud Leverage**: Cloud account/VPC separation, IAM, network segmentation

**Priority**: **CRITICAL** (if you develop software); **HIGH** (even for cloud configuration management)

**Cost**: $8,000-$20,000 (environment setup, access controls, data masking)

**Evidence**: Environment architecture, network segmentation, access control matrix, data masking configurations

---

#### A.8.32 Change Management

**Objective**: Manage changes to information processing facilities and systems.

**Your Implementation**:
- Change management process and policy
- Change request and approval (CAB - Change Advisory Board, or ISMS Manager approval)
- Testing before production deployment
- Rollback plan for every change
- Change logging and tracking
- Emergency change process (for critical incidents)

**Change Management Process**:
1. **Request**: Submit change request (description, justification, impact, risk)
2. **Assessment**: Assess risk, impact, resource needs
3. **Approval**: CAB or ISMS Manager approves (reject, approve, defer)
4. **Planning**: Plan implementation (schedule, resources, rollback)
5. **Testing**: Test change in non-production (if applicable)
6. **Implementation**: Execute change, monitor
7. **Verification**: Verify success, test rollback capability
8. **Documentation**: Update documentation, close change request
9. **Review**: Post-implementation review (lessons learned)

**Change Types**:
- **Standard**: Pre-approved, low-risk (e.g., regular patching)
- **Normal**: Requires approval, testing
- **Emergency**: Expedited approval for critical incidents

**Cloud Leverage**: Cloud deployment automation (CI/CD), infrastructure as code

**Priority**: **HIGH**

**Cost**: $5,000-$12,000 (change management process, tools, training)

**Evidence**: Change management policy, change request records, approvals, change logs

---

#### A.8.33 Test Information

**Objective**: Ensure appropriate selection and protection of test information.

**Your Implementation**:
- Use masked or synthetic data for testing (never real production data in dev/test)
- If production data required for testing, obtain approval and protect appropriately
- Delete test data after testing
- Test data retention policy

**Test Data Management**:
1. **Prefer**: Synthetic or masked data (no real PII)
2. **If production data needed**:
   - Obtain approval (ISMS Manager, Data Protection Officer)
   - Minimize data (only what's needed)
   - Mask PII
   - Access control (only authorized testers)
   - Delete after testing
   - Audit trail

**Data Masking for Testing**:
- Substitute PII with realistic but fake data
- Preserve data relationships (referential integrity)
- Anonymization or pseudonymization

**Cloud Leverage**: Cloud data masking tools, test data generation

**Priority**: **MEDIUM to HIGH** (especially if subject to GDPR)

**Cost**: $5,000-$12,000 (data masking, test data management process)

**Evidence**: Test data management policy, approval records for production data use, masking configurations

---

#### A.8.34 Protection of Information Systems during Audit Testing

**Objective**: Minimize impact of audit activities on operational systems.

**Your Implementation**:
- Plan audit activities (schedule, scope, duration)
- Use read-only access where possible (no changes to production during audits)
- Test audit procedures in non-production first
- Monitor audit activities (log auditor actions)
- Limit audit access (time-bound, need-to-know)
- Backup before invasive audit tests

**Audit Testing Controls**:
1. **Planning**: Agree on scope, timing, impact
2. **Read-Only**: Prefer viewing/reporting over changing
3. **Non-Production**: Test audit procedures in dev/test first
4. **Monitoring**: Log auditor access and activities
5. **Limitations**: Time-bound access, least privilege
6. **Backup**: Backup before invasive tests (e.g., vulnerability scans, pen tests)
7. **Revert**: Plan to revert changes if needed

**Penetration Testing**:
- Schedule during low-usage times
- Notify operations team
- Limit scope (authorized targets only)
- Monitor for unintended impact
- Stop if production impact detected

**Cloud Leverage**: Cloud read-only IAM roles for auditors

**Priority**: **MEDIUM**

**Cost**: $2,000-$5,000 (audit procedures, access controls)

**Evidence**: Audit planning documents, auditor access logs, read-only role configurations

---

## Summary: Annex A Implementation Priorities

### Critical Priorities (Implement First - Months 1-6)

**Quick Wins** (High impact, low effort):
1. A.5.17 - Multi-Factor Authentication (MFA)
2. A.8.13 - Information Backup
3. A.8.15 - Logging (enable on all systems)

**Foundation**:
4. A.5.1 - Information Security Policies
5. A.5.2 - Roles and Responsibilities
6. A.5.12 - Information Classification
7. A.5.15 - Access Control Policy
8. A.8.1 - Endpoint Security
9. A.8.7 - Anti-Malware Protection
10. A.8.24 - Encryption (data at rest and in transit)

### High Priorities (Months 3-9)

11. A.5.16 - Identity Management
12. A.5.18 - Access Rights Management
13. A.5.19-A.5.22 - Supplier/Third-Party Management
14. A.5.23 - Cloud Security
15. A.5.24-A.5.27 - Incident Response
16. A.8.2 - Privileged Access Management
17. A.8.8 - Vulnerability Management
18. A.8.16 - Security Monitoring (SIEM)
19. A.8.20 - Network Security
20. A.8.31 - Environment Separation (dev/test/prod)

### Medium Priorities (Months 6-12)

21. A.6.3 - Security Awareness Training
22. A.7.7 - Clear Desk/Clear Screen
23. A.7.9 - Off-Premises Asset Security (remote work)
24. A.8.3 - Information Access Restriction (RBAC)
25. A.8.6 - Capacity Management
26. A.8.9 - Configuration Management
27. A.8.12 - Data Leakage Prevention (DLP)
28. A.8.32 - Change Management

### Low Priorities or Leveraged (Months 9-15)

29. A.5.5-A.5.7 - Authority Contacts, Special Interest Groups, Threat Intelligence
30. A.7.1-A.7.14 - Physical Controls (mostly inherited from cloud)
31. A.8.11 - Data Masking
32. A.8.23 - Web Filtering
33. A.8.25-A.8.30 - Secure Development (if not developing software, N/A or apply to IaC)

---

## Leveraging Cloud Providers

**You can INHERIT approximately 35-40% of Annex A controls from cloud providers:**

**Fully Inherited** (cloud provider manages):
- A.7.1-A.7.14 - Most physical controls
- Portions of A.8.6 - Capacity Management (elastic scaling)
- Portions of A.8.11 - Equipment Maintenance (cloud infrastructure)
- Portions of A.8.14 - Redundancy (cloud high availability)

**Partially Leveraged** (cloud provides tools, you configure):
- A.5.23 - Cloud Security (shared responsibility)
- A.8.1 - Endpoint Security (cloud-based MDM)
- A.8.7 - Anti-Malware (cloud provider tools)
- A.8.8 - Vulnerability Management (cloud scanning tools)
- A.8.13 - Backups (cloud backup services)
- A.8.15 - Logging (cloud logging services)
- A.8.16 - Monitoring (cloud SIEM)
- A.8.20 - Network Security (cloud security groups, VPCs)
- A.8.24 - Encryption (cloud key management)

**How to Leverage**:
1. Collect cloud provider compliance reports (ISO 27001, SOC 2)
2. Reference provider controls in your SOA
3. Document shared responsibility model
4. Configure cloud security features appropriately
5. Verify cloud configurations meet your requirements

---

## Statement of Applicability (SOA)

After your risk assessment, you'll create a Statement of Applicability documenting which controls you:
- **Implement**: Control is necessary and implemented
- **Plan to Implement**: Control is necessary but not yet implemented (timeline)
- **Not Applicable**: Control doesn't apply to your organization (justify)
- **Alternative Control**: Different control achieves same objective

**SOA Example**:
| Control | Applicability | Justification | Implementation Status |
|---------|--------------|---------------|----------------------|
| A.5.17 MFA | Applicable | Critical for account security | Implemented (Month 2) |
| A.7.1 Physical Perimeter | N/A | Cloud-based, no physical infrastructure | Inherited from AWS |
| A.8.25 Secure SDLC | Not Applicable | No software development | N/A |

---

For detailed implementation roadmap and timeline, see:
- [Prioritized Roadmap](../roadmap/prioritized-roadmap.md)
- [Phase 1: Foundation](../roadmap/phase-1-foundation.md)
- [Quick Wins Guide](../roadmap/quick-wins.md)
