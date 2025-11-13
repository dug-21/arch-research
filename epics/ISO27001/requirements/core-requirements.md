# ISO 27001:2022 Core Requirements (Clauses 4-10)

## Overview

The core requirements (Clauses 4-10) form the mandatory management system framework for ISO 27001. These clauses establish the structure, processes, and governance for your Information Security Management System (ISMS).

**Key Principle**: All organizations seeking certification must implement ALL requirements in Clauses 4-10. Unlike Annex A controls (which are risk-based), these are non-negotiable.

---

## Clause 4: Context of the Organization

### 4.1 Understanding the Organization and Its Context

**Requirement**: Determine external and internal issues relevant to your purpose and affecting your ISMS.

**What This Means for You**:
- Identify business drivers for information security
- Understand regulatory requirements (GDPR, industry standards)
- Recognize client expectations (ISO 27001 certification requirement)
- Consider business dependencies (cloud providers, third parties)
- Assess organizational culture and maturity

**Practical Implementation**:
```
External Context:
- Client requirements for ISO 27001 certification
- B2B market competitive landscape
- Regulatory environment (data protection laws)
- Cybersecurity threat landscape
- Cloud provider ecosystem

Internal Context:
- Company size and structure
- Current security maturity (low - no formal processes)
- IT infrastructure (cloud-based, data rooms)
- Resource constraints
- Risk appetite
```

**Deliverables**:
- Context analysis document (2-4 pages)
- PESTLE analysis (optional: Political, Economic, Social, Technological, Legal, Environmental)

**Effort**: 1-2 days
**Cost**: $1,000-$2,000 (if using consultant)

---

### 4.2 Understanding the Needs and Expectations of Interested Parties

**Requirement**: Determine interested parties relevant to ISMS and their information security requirements.

**What This Means for You**:
Identify stakeholders who have interest in or influence over your information security.

**Key Interested Parties for Your Organization**:

| Stakeholder | Information Security Needs |
|-------------|---------------------------|
| B2B Clients | ISO 27001 certification, data confidentiality, availability |
| Non-profit associations | Donor data protection, compliance, trust |
| Employees | Secure systems, clear policies, job security |
| Leadership/Board | Business continuity, risk management, reputation |
| Cloud providers | Shared responsibility model, secure configuration |
| Third-party vendors | Security requirements in contracts |
| Regulators | GDPR, data protection law compliance |
| Certification body | ISO 27001 standard compliance |

**Practical Implementation**:
1. Create stakeholder matrix
2. Document requirements for each stakeholder
3. Review and validate with stakeholders
4. Update annually or when significant changes occur

**Deliverables**:
- Interested parties analysis (2-3 pages)
- Stakeholder requirements matrix

**Effort**: 1-2 days
**Cost**: $1,000-$2,000

---

### 4.3 Determining the Scope of the ISMS

**Requirement**: Define boundaries and applicability of the ISMS.

**Critical Decision**: What's in scope determines your certification effort and cost.

**Recommended Scope for Your Organization**:

**In Scope**:
- All cloud-hosted applications and services supporting B2B clients
- Data rooms containing client information
- Corporate IT systems (email, collaboration tools, identity management)
- Third-party integrations with client data access
- Remote employee access to systems
- Business locations: [List your offices]

**Out of Scope** (consider excluding initially):
- Physical archives (if minimal)
- HR systems not containing client data
- Personal devices (BYOD) - if you have MDM alternative
- Marketing websites with no customer data

**Scope Statement Template**:
```
The ISMS applies to:
- Organizational units: [All departments supporting B2B clients]
- Physical locations: [Office addresses]
- Information assets: Client data, intellectual property, business data
- Technology: Cloud services (AWS/Azure/GCP), SaaS applications,
  data rooms, identity management, employee endpoints
- Processes: Software development, client onboarding, data management,
  support services, third-party management

Exclusions:
- [Any systems/locations excluded with justification]
```

**Key Principles**:
- Include all systems processing client data
- Include all locations accessing scoped systems
- Be specific and clear
- Document rationale for exclusions
- Ensure scope meets client expectations

**Deliverables**:
- ISMS Scope Statement (2-3 pages)
- Scope diagram (visual representation)

**Effort**: 2-3 days
**Cost**: $2,000-$4,000

---

### 4.4 Information Security Management System

**Requirement**: Establish, implement, maintain, and continually improve an ISMS.

**What This Means**:
Create a systematic, documented approach to managing information security.

**ISMS Components**:

1. **Policies**: High-level direction and principles
2. **Procedures**: Step-by-step instructions for key processes
3. **Work Instructions**: Detailed task guidance
4. **Records**: Evidence of compliance
5. **Tools**: Systems supporting ISMS activities

**Implementation Approach**:

**Year 1 - Establish**:
- Define ISMS structure and documentation hierarchy
- Create core policies and procedures
- Implement foundational controls
- Train staff on ISMS requirements

**Year 2+ - Maintain & Improve**:
- Regular management reviews
- Internal audits
- Corrective actions
- Continuous improvement based on lessons learned

**Deliverables**:
- ISMS documentation structure
- Process map showing ISMS processes

**Effort**: Ongoing throughout program
**Cost**: Embedded in overall program

---

## Clause 5: Leadership

### 5.1 Leadership and Commitment

**Requirement**: Top management must demonstrate leadership and commitment to the ISMS.

**Top Management Responsibilities**:
- Ensure ISMS policy and objectives align with business strategy
- Integrate ISMS into business processes
- Provide resources (budget, people, tools)
- Communicate importance of information security
- Support continual improvement
- Support other management roles in their areas

**Practical Evidence**:
- Board/executive meeting minutes discussing ISMS
- Approved ISMS budget
- Executive endorsement of security policies
- Regular management reviews (at least annually)
- Executive participation in incident response

**Your Implementation**:
1. Present business case to CEO/Board (see Executive Summary)
2. Secure budget approval
3. Include ISMS in strategic planning
4. Executive sponsor for ISMS program
5. Quarterly steering committee meetings

**Deliverables**:
- Executive charter for ISMS
- Meeting minutes showing executive engagement

**Effort**: Ongoing - quarterly meetings
**Cost**: Executive time investment

---

### 5.2 Policy

**Requirement**: Top management shall establish an information security policy.

**Policy Requirements**:
- Appropriate to the purpose of the organization
- Include information security objectives
- Include commitment to satisfy applicable requirements
- Include commitment to continual improvement

**Sample Information Security Policy Structure**:

```
[Company Name] Information Security Policy

1. Purpose
   - Protect confidentiality, integrity, availability of information
   - Meet client requirements for ISO 27001 certification
   - Comply with legal and regulatory obligations

2. Scope
   - [Reference ISMS scope from 4.3]

3. Commitments
   - Implement risk-based approach to information security
   - Comply with ISO 27001 and applicable laws
   - Provide adequate resources for information security
   - Continually improve our ISMS
   - Respond to incidents effectively
   - Maintain business continuity capabilities

4. Roles and Responsibilities
   - Executive leadership: Oversight and resources
   - ISMS Manager: Day-to-day management
   - All employees: Follow security procedures

5. Policy Review
   - Reviewed annually or after significant changes

[CEO Signature]                    [Date]
```

**Deliverables**:
- Information Security Policy (2-3 pages)
- Evidence of approval (signature, board minutes)
- Communication to all staff (email, training)

**Effort**: 1-2 days to draft, 1-2 weeks for approvals
**Cost**: $1,500-$3,000

---

### 5.3 Organizational Roles, Responsibilities, and Authorities

**Requirement**: Assign and communicate information security roles and responsibilities.

**Key Roles for Your Organization**:

| Role | Responsibilities | Time Commitment |
|------|-----------------|----------------|
| **Executive Sponsor** (CEO/COO) | ISMS oversight, resource approval, management reviews | 2-4 hours/month |
| **ISMS Manager / CISO** | Day-to-day ISMS management, risk assessment, audits | 0.5-1.0 FTE |
| **IT Manager** | Technical controls, cloud security, access management | 0.3-0.5 FTE |
| **HR Manager** | People controls, training, background checks | 0.1 FTE |
| **Data Room Administrators** | Access control, audit logs, data classification | 0.2 FTE |
| **Third-Party Manager** | Vendor assessments, contract reviews | 0.1 FTE |
| **All Employees** | Follow security procedures, report incidents | Ongoing |

**Responsibilities Documentation**:

**ISMS Manager Responsibilities**:
- Lead ISMS implementation and maintenance
- Conduct risk assessments
- Coordinate internal audits
- Manage incident response
- Report to top management on ISMS performance
- Ensure ISMS conforms to ISO 27001
- Liaison with certification body

**Deliverables**:
- Roles and responsibilities matrix (1-2 pages)
- Job descriptions updated with security responsibilities
- RACI chart for ISMS processes

**Effort**: 2-3 days
**Cost**: $2,000-$4,000

---

## Clause 6: Planning

### 6.1 Actions to Address Risks and Opportunities

#### 6.1.1 General

**Requirement**: Plan actions to address risks and opportunities to ensure ISMS achieves intended outcomes.

**What This Means**:
- Identify what could go wrong (risks) or what opportunities exist
- Plan how to address them
- Integrate actions into ISMS processes

**Risks to Consider**:
- Information security risks (covered in 6.1.2)
- ISMS performance risks (e.g., insufficient resources, staff turnover)
- Business risks affecting information security

**Opportunities**:
- Automation to improve security and efficiency
- Cloud provider security features (cost-free enhancements)
- Security as competitive differentiator

---

#### 6.1.2 Information Security Risk Assessment

**Requirement**: Define and apply an information security risk assessment process.

**Risk Assessment Process Components**:

**1. Establish Risk Criteria**
```
Risk Appetite Statement:
[Company] has low tolerance for risks affecting:
- Client data confidentiality
- System availability for client services
- Compliance with legal/contractual obligations

Risk Acceptance Levels:
- Critical risks: Unacceptable - must remediate immediately
- High risks: Acceptable only with compensating controls and executive approval
- Medium risks: Acceptable with treatment plan within 6 months
- Low risks: Acceptable with monitoring
```

**2. Risk Assessment Methodology**

**Asset-Based Approach** (recommended for your maturity level):

**Step 1: Identify Information Assets**
- Client databases
- Data rooms
- Cloud applications
- Intellectual property
- Business data
- Employee access credentials

**Step 2: Identify Threats**
- External threats: Hackers, malware, ransomware, DDoS
- Internal threats: Accidental disclosure, insider abuse
- Environmental: Power outage, natural disaster (cloud data centers)
- Third-party: Cloud provider outage, vendor breach

**Step 3: Identify Vulnerabilities**
- Missing patches
- Weak passwords / no MFA
- Unencrypted data
- Excessive access privileges
- Lack of monitoring
- No backup testing

**Step 4: Assess Impact**
```
Impact Levels:
- Critical: Business-threatening, regulatory penalties, major client loss
- High: Significant client impact, reputation damage, financial loss
- Medium: Limited client impact, operational disruption
- Low: Minor inconvenience, no client impact
```

**Step 5: Assess Likelihood**
```
Likelihood Levels:
- Very Likely (>50%): Expected to occur within 1 year
- Likely (25-50%): May occur within 2 years
- Possible (10-25%): May occur within 5 years
- Unlikely (<10%): Rare occurrence
```

**Step 6: Calculate Risk Level**
```
Risk = Impact x Likelihood

Risk Matrix:
                Impact
              Low  Med  High  Critical
Unlikely      L    L    M     H
Possible      L    M    H     C
Likely        M    H    C     C
Very Likely   H    C    C     C

L = Low Risk
M = Medium Risk
H = High Risk
C = Critical Risk
```

**Example Risk**:
```
Risk: Ransomware attack on cloud infrastructure

Asset: Client databases
Threat: Ransomware
Vulnerability: No offline backups, limited endpoint protection
Impact: Critical (business disruption, data loss, client impact)
Likelihood: Likely (common threat, limited controls)
Risk Level: CRITICAL

Treatment: See 6.1.3 below
```

**Deliverables**:
- Risk assessment methodology document (5-10 pages)
- Asset inventory spreadsheet
- Risk register with 20-50 identified risks
- Risk assessment report

**Effort**: 5-10 days (workshops + documentation)
**Cost**: $8,000-$15,000

---

#### 6.1.3 Information Security Risk Treatment

**Requirement**: Define and apply an information security risk treatment process.

**Risk Treatment Options**:

1. **Modify the risk** (most common):
   - Implement security controls to reduce likelihood or impact
   - Example: Deploy MFA to reduce account compromise risk

2. **Retain the risk**:
   - Accept risk within defined criteria
   - Document rationale and management approval
   - Example: Accept low risk of physical break-in (cloud data centers)

3. **Avoid the risk**:
   - Eliminate the activity creating risk
   - Example: Discontinue storing certain types of sensitive data

4. **Share the risk**:
   - Transfer to third party (insurance, cloud provider SLAs)
   - Example: Cyber insurance for breach response costs

**Risk Treatment Plan**:

| Risk ID | Risk Description | Risk Level | Treatment Option | Controls | Owner | Due Date | Residual Risk |
|---------|-----------------|------------|------------------|----------|-------|----------|---------------|
| R-001 | Account compromise due to weak passwords | Critical | Modify | Implement MFA, password policy | IT Manager | Month 2 | Low |
| R-005 | Data breach from unauthorized access | High | Modify | RBAC, access reviews, logging | ISMS Manager | Month 4 | Medium |
| R-012 | Cloud provider outage | Medium | Share | Multi-region deployment, SLA | IT Manager | Month 8 | Low |
| R-023 | Minor data misclassification | Low | Retain | Document, monitor, train | Data Owner | N/A | Low |

**Residual Risk**:
- Risk level remaining after controls implemented
- Must be accepted by management
- Documented in risk treatment plan

**Deliverables**:
- Risk treatment plan (spreadsheet or ISMS tool)
- Management approval of risk treatment decisions
- Management acceptance of residual risks

**Effort**: 3-5 days
**Cost**: $4,000-$8,000

---

### 6.2 Information Security Objectives and Planning to Achieve Them

**Requirement**: Establish information security objectives at relevant functions and levels.

**Objective Characteristics (SMART)**:
- **S**pecific
- **M**easurable
- **A**chievable
- **R**elevant
- **T**ime-bound

**Sample Information Security Objectives for Your Organization**:

```
Objective 1: Achieve ISO 27001 Certification
- Measure: Certificate issued
- Target: Within 18 months of program start
- Owner: ISMS Manager
- Resources: Budget, consultant, staff time

Objective 2: Implement Multi-Factor Authentication
- Measure: 100% of user accounts have MFA enabled
- Target: Within 3 months
- Owner: IT Manager
- Resources: MFA tool licensing, user training

Objective 3: Security Awareness Training
- Measure: 95% of staff complete annual training
- Target: All staff trained within 90 days of hire; annual refresher
- Owner: ISMS Manager
- Resources: Training platform, content development

Objective 4: Vendor Security Assessments
- Measure: 100% of high-risk vendors assessed
- Target: Within 6 months; annual review thereafter
- Owner: Third-Party Manager
- Resources: Questionnaire template, assessment time

Objective 5: Incident Response Time
- Measure: 100% of incidents acknowledged within 1 hour,
  initial triage within 4 hours
- Target: Ongoing
- Owner: IT Manager
- Resources: On-call rotation, incident response tools

Objective 6: Data Room Access Controls
- Measure: 100% of data rooms have RBAC, audit logging enabled
- Target: Within 5 months
- Owner: Data Room Administrator
- Resources: Configuration time, access review process
```

**Planning to Achieve Objectives**:
For each objective, document:
- What will be done
- What resources required
- Who is responsible
- When it will be completed
- How results will be evaluated

**Deliverables**:
- Information security objectives document (2-3 pages)
- Implementation plans for each objective
- Regular progress tracking (monthly)

**Effort**: 2-3 days initially; ongoing monitoring
**Cost**: $2,000-$4,000

---

### 6.3 Planning of Changes

**Requirement**: When changes to the ISMS are needed, they shall be carried out in a planned manner.

**What This Means**:
Don't make ad-hoc changes to the ISMS. Plan, assess risks, communicate, and document.

**Change Scenarios Requiring Planning**:
- Scope changes (adding new systems, locations)
- Organizational changes (mergers, acquisitions, restructuring)
- Technology changes (new cloud services, applications)
- Control changes (implementing new security tools)
- Process changes (new policies, procedures)

**Change Process**:
1. Identify need for change
2. Assess impact on ISMS (risks, resources, objectives)
3. Obtain approval (ISMS Manager or management)
4. Plan implementation (resources, timeline, communication)
5. Implement change
6. Verify effectiveness
7. Update ISMS documentation

**Practical Example**:
```
Change: Migrating from on-premise data rooms to SaaS data room solution

Planning:
1. Security review of new vendor
2. Data migration plan
3. Access control configuration
4. Update policies and procedures
5. Train staff
6. Update ISMS scope (if vendor location changes)
7. Update risk assessment
8. Update Statement of Applicability
```

**Deliverables**:
- Change management procedure (2-3 pages)
- Change request form template
- Change log (spreadsheet)

**Effort**: 1-2 days for procedure; ongoing for changes
**Cost**: $1,500-$3,000

---

## Clause 7: Support

### 7.1 Resources

**Requirement**: Determine and provide resources needed for establishment, implementation, maintenance, and continual improvement of the ISMS.

**Resources to Consider**:

**People**:
- ISMS Manager (0.5-1.0 FTE)
- IT staff for technical controls
- Support from HR, legal, finance
- Consultant support (as needed)

**Budget**:
- See Executive Summary for detailed budget
- Year 1: $105,000-$175,000
- Ongoing: $25,000-$45,000/year

**Technology**:
- ISMS documentation platform (optional)
- Security tools (MFA, logging, monitoring)
- Cloud provider security features (already included)
- Training platform

**Time**:
- 18 months to certification
- Ongoing maintenance

**Deliverables**:
- Resource allocation document
- Budget approval
- Staffing plan

**Effort**: Embedded in planning
**Cost**: See budget in Executive Summary

---

### 7.2 Competence

**Requirement**: Ensure persons doing work under the organization's control affecting information security are competent.

**Competence Requirements**:

| Role | Required Competence | How to Achieve |
|------|-------------------|---------------|
| ISMS Manager | ISO 27001 knowledge, risk management, audit | Certification training (5 days, $3,000-$5,000) |
| IT Manager | Cloud security, access control, monitoring | Cloud certifications, vendor training |
| Data Room Admins | Data classification, access control | Internal training, procedures |
| All Staff | Security awareness | Annual training (online, 1 hour) |

**Implementation Steps**:
1. Define competence requirements for each role
2. Assess current competence (gaps)
3. Provide training to close gaps
4. Maintain training records
5. Evaluate effectiveness (tests, observations)

**Training Plan**:
- ISMS Manager: ISO 27001 Lead Implementer (1 week)
- IT Staff: Cloud security, incident response (vendor courses)
- All Staff: Security awareness (annual, 1 hour online)
- Specialized: Incident response, forensics (as needed)

**Deliverables**:
- Competence requirements by role
- Training plan
- Training records (attendance, completion certificates)

**Effort**: 2-3 days planning; ongoing training delivery
**Cost**: $5,000-$10,000 initially; $2,000-$4,000/year ongoing

---

### 7.3 Awareness

**Requirement**: Ensure persons doing work under the organization's control are aware of information security policy, their contribution to ISMS effectiveness, and implications of not conforming.

**Awareness Program Components**:

**1. Initial Onboarding**:
- ISMS overview
- Information security policy
- Role-specific responsibilities
- How to report incidents
- Acceptable use policy

**2. Annual Training**:
- Security threats update (phishing, ransomware)
- Data handling best practices
- Password and MFA usage
- Incident examples and lessons learned
- Policy updates

**3. Ongoing Communications**:
- Monthly security tips (email, Slack)
- Incident alerts (real-time)
- Posters and reminders (physical/digital)
- Simulated phishing exercises (quarterly)

**4. Specialized Training**:
- Data room administrators: Access control, audit logs
- Developers: Secure coding (if applicable)
- Third-party managers: Vendor assessments

**Awareness Metrics**:
- 95% training completion rate
- Phishing click rate <5%
- Security incident reporting within 1 hour

**Deliverables**:
- Awareness program plan
- Training materials (slides, videos, handouts)
- Training records
- Awareness metrics dashboard

**Effort**: 5-7 days to develop; 1-2 days/year to deliver
**Cost**: $8,000-$12,000 initially; $2,000-$4,000/year ongoing

---

### 7.4 Communication

**Requirement**: Determine internal and external communications relevant to the ISMS.

**Communication Plan**:

| What to Communicate | To Whom | When | How | Owner |
|-------------------|---------|------|-----|-------|
| ISMS launch | All staff | Program start | Email, town hall | ISMS Manager |
| Policy updates | All staff | As policies approved | Email, intranet | ISMS Manager |
| Security incidents | Relevant staff, management | Real-time | Incident alert system | IT Manager |
| Training requirements | All staff | Quarterly | Email, LMS notifications | ISMS Manager |
| Audit results | Management, staff | After audits | Report, meeting | ISMS Manager |
| Certification achievement | Clients, staff, market | Upon certification | Press release, website | Marketing |
| Management review | Top management | Annually | Formal meeting | ISMS Manager |
| Vendor security requirements | Third parties | Contract start | Contract clauses | Procurement |

**Communication Channels**:
- Email
- Intranet / SharePoint
- Team meetings
- Incident response system
- Client portal (for external)

**Deliverables**:
- Communication plan (2-3 pages)
- Communication templates (incident alert, policy update, etc.)
- Communication records (sent emails, meeting minutes)

**Effort**: 2-3 days
**Cost**: $2,000-$4,000

---

### 7.5 Documented Information

**Requirement**: The ISMS shall include documented information required by ISO 27001 and determined necessary by the organization for ISMS effectiveness.

**Mandatory Documented Information** (ISO 27001 requires):

| Document | ISO 27001 Reference | Description |
|----------|-------------------|-------------|
| ISMS Scope | 4.3 | Boundaries and applicability |
| Information Security Policy | 5.2 | Top management commitment |
| Risk Assessment Methodology | 6.1.2 | How risks are assessed |
| Risk Treatment Plan | 6.1.3 | How risks are treated |
| Statement of Applicability | 6.1.3(d) | Which Annex A controls apply |
| Competence Records | 7.2 | Training, skills, experience |
| Operational Planning | 8.1 | How controls are implemented |
| Risk Assessment Results | 8.2 | Output of risk assessments |
| Risk Treatment Results | 8.3 | Implementation evidence |
| Monitoring and Measurement | 9.1 | What and how to measure |
| Internal Audit Program | 9.2 | Audit plans and procedures |
| Audit Results | 9.2 | Findings from audits |
| Management Review Results | 9.3 | Decisions from reviews |
| Nonconformities & Corrective Actions | 10.1 | Issues and resolutions |

**Additional Documentation You'll Need**:
- Security policies (10-15 core policies)
- Procedures (incident response, access management, change control, etc.)
- Work instructions (how-to guides)
- Forms and templates
- Records (logs, approvals, reviews)

**Documentation Hierarchy**:
```
Level 1: Information Security Policy (executive-level)
  |
  |-- Level 2: Security Policies (topic-specific, 10-15 policies)
       |
       |-- Level 3: Procedures (step-by-step, 15-25 procedures)
            |
            |-- Level 4: Work Instructions (detailed guides)
                 |
                 |-- Level 5: Records (evidence, logs)
```

**Document Control Requirements**:
- Version control
- Approval process
- Review and update cycle
- Access control (who can view/edit)
- Retention periods

**Tools**:
- SharePoint / Google Drive (with permissions)
- ISMS platform (Vanta, Drata, etc.) - automates much of this
- Document management system

**Deliverables**:
- Document inventory (spreadsheet)
- Document control procedure
- All mandatory documentation (see table above)
- Template library

**Effort**: Ongoing throughout program - 20-30% of total effort
**Cost**: Embedded in overall program costs

---

## Clause 8: Operation

### 8.1 Operational Planning and Control

**Requirement**: Plan, implement, and control processes needed to meet information security requirements and implement actions determined in Clause 6.

**What This Means**:
Actually implement the controls you decided on in your risk treatment plan.

**Implementation Approach**:

**For Each Control in Risk Treatment Plan**:
1. Define implementation requirements
2. Assign owner and resources
3. Create timeline
4. Implement control
5. Document implementation (evidence)
6. Test effectiveness
7. Update relevant documentation

**Example: Implementing MFA**:
```
Control: Multi-Factor Authentication (Annex A.5.17, A.5.18)

Planning:
- Select MFA solution (Microsoft Authenticator, Google Auth, etc.)
- Pilot with IT team (2 weeks)
- Communicate to all staff (email, training)
- Rollout schedule (department by department, 6 weeks)
- Support process (helpdesk, documentation)

Implementation:
- Configure MFA in identity provider (Azure AD, Okta, etc.)
- Enroll users
- Enforce MFA policy
- Monitor adoption

Control:
- Track MFA enrollment (target: 100%)
- Monitor MFA bypass attempts
- Review exceptions monthly

Evidence:
- Configuration screenshots
- Enrollment reports
- MFA policy document
- User training records
```

**Deliverables**:
- Implementation plans for each control
- Control implementation evidence
- Updated procedures

**Effort**: Varies by control - major portion of program
**Cost**: See Phase 2 budget in Executive Summary

---

### 8.2 Information Security Risk Assessment

**Requirement**: Perform information security risk assessments at planned intervals or when significant changes occur.

**Risk Assessment Schedule**:
- **Initial**: During ISMS implementation (Months 2-4)
- **Recurring**: Annually (or after significant changes)
- **Triggered**: When major changes occur

**Triggers for Risk Assessment**:
- New systems or services
- Major organizational changes
- Significant incidents
- Major threat landscape changes
- New legal/regulatory requirements
- Client requirements change

**Process**:
1. Review previous risk assessment
2. Identify changes since last assessment
3. Conduct risk assessment (using methodology from 6.1.2)
4. Update risk register
5. Report results to management
6. Update risk treatment plan (if needed)

**Deliverables**:
- Updated risk assessment (annually)
- Risk assessment records

**Effort**: 3-5 days initially; 2-3 days annually
**Cost**: $4,000-$8,000 initially; $2,000-$4,000 annually

---

### 8.3 Information Security Risk Treatment

**Requirement**: Implement the information security risk treatment plan.

**What This Means**:
Execute the plan you created in 6.1.3. This is where controls get implemented.

**Implementation Tracking**:
- Use risk treatment plan as project plan
- Track status of each control implementation
- Update residual risk as controls are implemented
- Document evidence of implementation

**Evidence Examples**:
- Configuration screenshots
- Policy approval signatures
- Training completion reports
- Access control matrices
- Audit log samples
- Vendor contracts with security clauses

**Deliverables**:
- Implemented controls (per risk treatment plan)
- Implementation evidence
- Updated residual risk levels

**Effort**: Major effort - see Phase 1 and 2 in roadmap
**Cost**: See roadmap budget

---

## Clause 9: Performance Evaluation

### 9.1 Monitoring, Measurement, Analysis, and Evaluation

**Requirement**: Determine what needs to be monitored and measured, how, and when.

**Key ISMS Metrics** (examples):

| Metric Category | What to Measure | Target | Frequency |
|----------------|----------------|--------|-----------|
| **Availability** | System uptime | 99.9% | Real-time |
| **Incidents** | Number of security incidents | Trending down | Monthly |
| **Incidents** | Mean time to respond | <4 hours | Per incident |
| **Access Control** | Privileged access reviews completed | 100% quarterly | Quarterly |
| **Training** | Staff training completion | 95% | Quarterly |
| **Vulnerabilities** | Critical vulnerabilities patched | 100% within 7 days | Weekly |
| **Audit** | Audit findings closed | 100% by due date | Per audit |
| **Controls** | Controls tested and effective | 95% | Annually |

**Monitoring Mechanisms**:
- Security Information and Event Management (SIEM) - cloud provider tools
- Vulnerability scanning (monthly)
- Access reviews (quarterly)
- Training tracking (LMS platform)
- Incident tracking system
- Compliance dashboard (ISMS tool)

**Analysis and Reporting**:
- Monthly ISMS metrics report
- Quarterly management dashboard
- Annual ISMS performance report

**Deliverables**:
- Monitoring and measurement plan (3-5 pages)
- Metrics dashboard
- Regular metric reports

**Effort**: 3-5 days setup; ongoing monitoring
**Cost**: $4,000-$8,000 setup; included in ISMS tools

---

### 9.2 Internal Audit

**Requirement**: Conduct internal audits at planned intervals to verify ISMS conforms to ISO 27001 and is effectively implemented.

**Internal Audit Program**:

**Frequency**: At least annually (before certification audit)

**Scope**: Cover all ISMS processes and controls over audit cycle

**Audit Planning**:
```
Year 1 (Pre-certification):
- Month 10-11: Internal audit covering all clauses and controls
- Month 13-14: Follow-up audit for any findings

Year 2+ (Post-certification):
- Quarterly: Rotating audits (25% of ISMS each quarter)
- Annual: Comprehensive audit before surveillance
```

**Audit Process**:
1. Develop audit plan and scope
2. Select auditors (must be independent - not auditing own work)
3. Conduct opening meeting
4. Review documents
5. Conduct interviews
6. Test control effectiveness (sampling)
7. Document findings (nonconformities, observations)
8. Closing meeting
9. Issue audit report
10. Track corrective actions

**Auditor Options**:
- **Internal staff** (trained in ISO 27001 auditing)
  - Cost: Training ($2,000-$4,000) + time
  - Benefit: Lower cost, better context
  - Risk: Less independent perspective

- **External auditor** (consultant or certification body)
  - Cost: $5,000-$10,000 per audit
  - Benefit: Independent, expert perspective
  - Risk: Higher cost

**Recommendation**: Use external auditor for first internal audit (Year 1), then train internal staff for ongoing audits.

**Audit Findings Types**:
- **Major nonconformity**: ISO 27001 requirement not met
- **Minor nonconformity**: Isolated lapse or weakness
- **Observation**: Opportunity for improvement
- **Good practice**: Positive finding

**Deliverables**:
- Internal audit program (procedure)
- Annual audit plan
- Audit reports
- Corrective action plan
- Follow-up audit reports

**Effort**: 3-5 days per comprehensive audit
**Cost**: $5,000-$10,000 (external); $2,000-$4,000 (internal)

---

### 9.3 Management Review

**Requirement**: Top management shall review the ISMS at planned intervals to ensure continuing suitability, adequacy, and effectiveness.

**Management Review Frequency**: At least annually (recommend semi-annually in Year 1)

**Review Inputs** (what management needs to review):
1. Status of actions from previous reviews
2. Changes in external and internal issues (context)
3. Feedback on information security performance (metrics)
4. Feedback from interested parties (clients, employees)
5. Risk assessment and risk treatment results
6. Opportunities for continual improvement
7. Audit results (internal and external)
8. Performance against information security objectives
9. Nonconformities and corrective actions
10. Monitoring and measurement results
11. Changes that could affect the ISMS

**Review Outputs** (management decisions):
1. Opportunities for continual improvement
2. Any need for changes to the ISMS
3. Resource needs

**Management Review Meeting Structure**:
```
Agenda (2-3 hours):
1. Opening and review of previous actions (15 min)
2. ISMS performance review (45 min)
   - Metrics dashboard
   - Incidents and trends
   - Audit results
3. Risk landscape update (30 min)
   - New/changed risks
   - Control effectiveness
4. Stakeholder feedback (15 min)
   - Client feedback
   - Employee feedback
5. Objectives review (15 min)
   - Progress against objectives
6. Resource and budget (15 min)
7. Decisions and action items (15 min)
8. Closing
```

**Attendees**:
- Executive sponsor (CEO/COO)
- ISMS Manager
- IT Manager
- Other relevant management (HR, Finance)

**Deliverables**:
- Management review procedure
- Management review meeting minutes
- Action item tracking
- Evidence of management decisions

**Effort**: 1 day preparation; 2-3 hour meeting
**Cost**: Management time investment; $1,000-$2,000 for report preparation

**Frequency**:
- Year 1: Quarterly (4 reviews) - during implementation
- Year 2+: Semi-annually or annually

---

## Clause 10: Improvement

### 10.1 Nonconformity and Corrective Action

**Requirement**: When a nonconformity occurs, take action to control and correct it, and deal with consequences.

**Nonconformity**: Failure to meet an ISMS requirement (ISO 27001, policy, procedure).

**Sources of Nonconformities**:
- Internal audits
- External audits (certification body)
- Incidents
- Monitoring and measurement
- Management review

**Corrective Action Process**:

**1. Detect Nonconformity**:
- Audit finding
- Incident investigation
- Control failure

**2. React**:
- Control the nonconformity (immediate action)
- Deal with consequences (damage control)

**3. Evaluate**:
- Determine root cause (5 Whys, fishbone analysis)
- Assess if similar nonconformities exist elsewhere

**4. Implement Corrective Action**:
- Eliminate root cause
- Prevent recurrence
- Implement systemic fixes

**5. Review Effectiveness**:
- Verify corrective action worked
- Close nonconformity

**6. Update ISMS**:
- Update risk assessment (if risks changed)
- Update procedures (if process caused issue)
- Update training (if competence gap)

**Example**:
```
Nonconformity: Privileged access review not completed quarterly (required by procedure)

Root Cause:
- Process owner unclear
- No reminder system
- Conflicting priorities

Corrective Action:
- Assign clear process owner (IT Manager)
- Implement automated reminders (calendar, task system)
- Add to management dashboard (visibility)
- Update procedure with owner and reminder process

Effectiveness Review (3 months later):
- Next two quarterly reviews completed on time
- Dashboard shows green status
- Nonconformity closed
```

**Deliverables**:
- Nonconformity and corrective action procedure
- Corrective action register (tracking spreadsheet)
- Root cause analysis documents
- Effectiveness review evidence

**Effort**: Varies per nonconformity; 1-5 days typically
**Cost**: Embedded in ISMS operations

---

### 10.2 Continual Improvement

**Requirement**: Continually improve the suitability, adequacy, and effectiveness of the ISMS.

**What This Means**:
The ISMS should get better over time. Learn from incidents, audits, metrics, and feedback.

**Improvement Opportunities**:
- Audit findings (internal and external)
- Incident lessons learned
- New threats or technologies
- Process inefficiencies
- Employee feedback
- Client feedback
- Industry best practices

**Improvement Examples**:

**Process Improvement**:
- Automate manual security processes (e.g., access provisioning)
- Streamline incident response based on lessons learned
- Improve training effectiveness (interactive vs. slide-based)

**Technology Improvement**:
- Upgrade to better security tools
- Leverage new cloud provider features
- Implement automation (SOAR - Security Orchestration, Automation, Response)

**Maturity Improvement**:
- Reactive to proactive security posture
- Manual to automated processes
- Compliance-driven to risk-driven

**Improvement Process**:
1. Identify improvement opportunity
2. Assess feasibility and benefits
3. Obtain approval (if resources required)
4. Implement improvement
5. Measure effectiveness
6. Standardize and document

**Continual Improvement Metrics**:
- Number of improvement initiatives per year
- Cost savings from automation
- Risk reduction over time
- Incident reduction year-over-year
- Audit findings reduction
- Employee security awareness improvement

**Deliverables**:
- Improvement register (tracking improvements)
- Annual improvement plan
- Improvement effectiveness reports

**Effort**: Ongoing - 10-15% of ISMS effort
**Cost**: Varies by improvement; budget 10-15% annually

---

## Implementation Timeline (Core Requirements)

| Clause | Requirement | Timeline | Effort | Dependencies |
|--------|------------|----------|--------|--------------|
| 4.1-4.2 | Context and stakeholders | Month 1 | 2-3 days | None |
| 4.3 | ISMS scope | Month 1-2 | 2-3 days | 4.1-4.2 complete |
| 5.1-5.2 | Leadership, policy | Month 1-2 | 2-3 days | 4.3 complete |
| 5.3 | Roles and responsibilities | Month 2 | 2-3 days | 5.2 complete |
| 6.1.2 | Risk assessment | Month 2-4 | 5-10 days | 4.3 complete |
| 6.1.3 | Risk treatment | Month 3-5 | 3-5 days | 6.1.2 complete |
| 6.2 | Objectives | Month 3-4 | 2-3 days | 6.1.3 complete |
| 7.2-7.3 | Competence, awareness | Month 3-6 | 5-7 days | 5.3 complete |
| 7.5 | Documentation | Ongoing | 20-30% | All clauses |
| 8.1-8.3 | Operations (implement controls) | Month 6-12 | Major effort | 6.1.3 complete |
| 9.1 | Monitoring and measurement | Month 6-12 | 3-5 days | 8.1 started |
| 9.2 | Internal audit | Month 10-12 | 3-5 days | 8.3 substantially complete |
| 9.3 | Management review | Month 12 | 1 day | 9.2 complete |
| 10.1-10.2 | Improvement | Ongoing | Ongoing | 9.3 complete |

---

## Quick Reference Checklist

### Clause 4: Context
- [ ] Context analysis complete
- [ ] Interested parties identified
- [ ] ISMS scope defined and approved
- [ ] ISMS framework established

### Clause 5: Leadership
- [ ] Executive commitment secured
- [ ] Information security policy approved
- [ ] Roles and responsibilities assigned

### Clause 6: Planning
- [ ] Risk assessment methodology defined
- [ ] Risk assessment conducted
- [ ] Risk treatment plan created
- [ ] Information security objectives set
- [ ] Change management process defined

### Clause 7: Support
- [ ] Resources allocated (budget, people)
- [ ] Competence requirements defined
- [ ] Training delivered
- [ ] Awareness program implemented
- [ ] Communication plan in place
- [ ] Documentation structure established

### Clause 8: Operation
- [ ] Controls implemented per risk treatment plan
- [ ] Implementation evidence collected
- [ ] Processes operational

### Clause 9: Performance Evaluation
- [ ] Monitoring and measurement implemented
- [ ] Internal audit completed
- [ ] Management review conducted
- [ ] Metrics tracked and reported

### Clause 10: Improvement
- [ ] Corrective action process operational
- [ ] Improvements identified and implemented
- [ ] ISMS continuously improving

---

## Additional Resources

See companion documents:
- [Annex A Controls Breakdown](annex-a-controls.md)
- [Documentation Requirements](documentation-requirements.md)
- [Certification Process](certification-process.md)
- [Prioritized Roadmap](../roadmap/prioritized-roadmap.md)
