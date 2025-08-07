-- Sample Data for Business Process Inventory Database
-- This script populates the database with realistic example data based on payment industry processes

-- =====================================================
-- Reference Data Setup
-- =====================================================

-- Insert Organizations
INSERT INTO organizations (name, organization_type, description) VALUES
('Global Payments Corp', 'enterprise', 'Top-level organization'),
('Payment Operations Division', 'division', 'Core payment processing operations'),
('Customer Operations Department', 'department', 'Customer onboarding and service'),
('Technology Department', 'department', 'IT systems and development'),
('Risk & Compliance Department', 'department', 'Risk management and regulatory compliance'),
('Finance Operations Department', 'department', 'Financial operations and reconciliation');

-- Insert Process Categories
INSERT INTO process_categories (category_code, name, description, display_order) VALUES
('TRANS', 'Transaction Processing', 'Core transaction handling and processing flows', 1),
('COMP', 'Compliance & Risk', 'Regulatory compliance and risk management processes', 2),
('CUST', 'Customer Operations', 'Customer-facing operational processes', 3),
('INTERNAL', 'Internal Operations', 'Back-office and operational support processes', 4),
('INTEGRATION', 'Integration & Orchestration', 'System integration and process orchestration', 5);

-- Insert Sub-categories
INSERT INTO process_categories (category_code, name, description, parent_category_id, display_order) VALUES
('TRANS-AUTH', 'Authorization Flows', 'Payment authorization and approval processes', 1, 1),
('TRANS-SETTLE', 'Settlement Processing', 'Transaction settlement and clearing processes', 1, 2),
('TRANS-CROSSBORDER', 'Cross-Border Payments', 'International payment processing', 1, 3),
('COMP-KYC', 'KYC/AML', 'Customer identification and anti-money laundering', 2, 1),
('COMP-RISK', 'Risk Management', 'Risk assessment and mitigation processes', 2, 2),
('CUST-ONBOARD', 'Customer Onboarding', 'New customer setup and verification', 3, 1),
('CUST-SUPPORT', 'Customer Support', 'Customer service and issue resolution', 3, 2),
('INTERNAL-RECON', 'Reconciliation', 'Financial reconciliation processes', 4, 1),
('INTERNAL-REPORT', 'Reporting', 'Management and regulatory reporting', 4, 2);

-- Insert Systems
INSERT INTO systems (system_code, name, description, system_type, vendor, version, status, criticality, owner_contact, support_contact) VALUES
('CRM-001', 'Customer Relationship Management', 'Primary customer data and interaction system', 'core', 'Salesforce', '2023.1', 'production', 'critical', 'crm-admin@company.com', 'crm-support@company.com'),
('PAY-001', 'Payment Processing Engine', 'Core payment processing and routing system', 'core', 'Internal', '3.2.1', 'production', 'critical', 'payments-admin@company.com', 'payments-support@company.com'),
('FRAUD-001', 'Fraud Detection System', 'Real-time fraud screening and risk scoring', 'supporting', 'FICO', '8.1.2', 'production', 'critical', 'fraud-admin@company.com', 'fraud-support@company.com'),
('GL-001', 'General Ledger', 'Financial reporting and accounting system', 'core', 'SAP', '9.3', 'production', 'critical', 'finance-admin@company.com', 'sap-support@company.com'),
('IDV-001', 'Identity Verification', 'Customer identity verification service', 'integration', 'Jumio', '2.1', 'production', 'high', 'idv-admin@company.com', 'jumio-support@company.com'),
('SWIFT-001', 'SWIFT Network', 'International messaging and settlement', 'external', 'SWIFT', '2023.R1', 'production', 'critical', 'swift-admin@company.com', 'swift-support@company.com'),
('RECON-001', 'Reconciliation Engine', 'Automated reconciliation platform', 'supporting', 'SmartStream', '4.2', 'production', 'high', 'recon-admin@company.com', 'recon-support@company.com'),
('NOTIFY-001', 'Notification Service', 'Email and SMS notification platform', 'supporting', 'SendGrid', '3.0', 'production', 'medium', 'notify-admin@company.com', 'sendgrid-support@company.com');

-- Insert Stakeholders
INSERT INTO stakeholders (employee_id, first_name, last_name, email, phone, title, department, organization_id, is_active) VALUES
('EMP001', 'Jane', 'Smith', 'jane.smith@company.com', '+1-555-0101', 'VP Customer Operations', 'Customer Operations Department', 3, true),
('EMP002', 'Michael', 'Johnson', 'michael.johnson@company.com', '+1-555-0102', 'Payment Systems Manager', 'Technology Department', 4, true),
('EMP003', 'Sarah', 'Chen', 'sarah.chen@company.com', '+1-555-0103', 'Finance Operations Manager', 'Finance Operations Department', 6, true),
('EMP004', 'David', 'Liu', 'david.liu@company.com', '+1-555-0104', 'International Payments Manager', 'Payment Operations Division', 2, true),
('EMP005', 'Lisa', 'Brown', 'lisa.brown@company.com', '+1-555-0105', 'Compliance Officer', 'Risk & Compliance Department', 5, true),
('EMP006', 'Mike', 'Jones', 'mike.jones@company.com', '+1-555-0106', 'Senior Customer Analyst', 'Customer Operations Department', 3, true),
('EMP007', 'Alex', 'Kumar', 'alex.kumar@company.com', '+1-555-0107', 'Senior Payment Engineer', 'Technology Department', 4, true),
('EMP008', 'Priya', 'Patel', 'priya.patel@company.com', '+1-555-0108', 'Risk Analyst', 'Risk & Compliance Department', 5, true),
('EMP009', 'Robert', 'Kim', 'robert.kim@company.com', '+1-555-0109', 'Senior Financial Analyst', 'Finance Operations Department', 6, true),
('EMP010', 'Emma', 'Taylor', 'emma.taylor@company.com', '+1-555-0110', 'Treasury Analyst', 'Finance Operations Department', 6, true);

-- Set up manager relationships
UPDATE stakeholders SET manager_stakeholder_id = 1 WHERE stakeholder_id = 6;  -- Mike reports to Jane
UPDATE stakeholders SET manager_stakeholder_id = 2 WHERE stakeholder_id = 7;  -- Alex reports to Michael
UPDATE stakeholders SET manager_stakeholder_id = 3 WHERE stakeholder_id = 9;  -- Robert reports to Sarah
UPDATE stakeholders SET manager_stakeholder_id = 3 WHERE stakeholder_id = 10; -- Emma reports to Sarah
UPDATE stakeholders SET manager_stakeholder_id = 5 WHERE stakeholder_id = 8;  -- Priya reports to Lisa

-- =====================================================
-- Core Processes
-- =====================================================

-- Insert Main Processes
INSERT INTO processes (
    process_code, name, description, purpose, scope_description, version, status,
    category_id, sub_category, business_priority, risk_level,
    owner_stakeholder_id, backup_owner_stakeholder_id, organization_id,
    frequency, average_duration_minutes, min_duration_minutes, max_duration_minutes,
    average_volume, peak_volume, volume_unit, volume_period,
    current_success_rate, target_success_rate,
    automation_level, customer_impact, revenue_impact,
    security_classification, is_regulatory_required, is_audit_trail_required,
    has_seasonal_variation, process_maturity_level
) VALUES

-- Customer Onboarding Process
('PROC-001', 
 'Customer Onboarding', 
 'Complete process for registering new customers including identity verification, risk assessment, and account setup',
 'Enable new customers to access payment services while ensuring regulatory compliance and risk management',
 'Covers individual and business customer onboarding from application to account activation',
 '1.2', 'active', 7, 'New Customer Setup', 'high', 'medium',
 1, 6, 3, 'daily', 45, 30, 120,
 75, 200, 'applications', 'day',
 95.2, 98.0, 'semi-automated', 'critical', 'indirect',
 'confidential', true, true, true, 'defined'),

-- Payment Authorization Process  
('PROC-002',
 'Payment Authorization',
 'Real-time authorization of card-based payments including fraud screening and fund verification',
 'Approve or decline payment requests while minimizing fraud and maximizing legitimate transaction acceptance',
 'Covers all card-based payment authorizations including credit, debit, and prepaid cards',
 '2.1', 'active', 3, 'Card Authorization', 'critical', 'high',
 2, 7, 4, 'continuous', 2, 1, 10,
 25000, 100000, 'transactions', 'hour',
 92.3, 95.0, 'fully-automated', 'critical', 'direct',
 'confidential', true, true, false, 'optimized'),

-- Settlement Reconciliation Process
('PROC-003',
 'Settlement Reconciliation',
 'Daily matching of processed transactions with network settlements and fee calculations',
 'Ensure accurate financial reporting and identify discrepancies in transaction processing',
 'Covers daily reconciliation of all payment networks and internal transaction records',
 '1.8', 'active', 9, 'Daily Reconciliation', 'high', 'medium',
 3, 9, 6, 'daily', 120, 90, 180,
 2500, 5000, 'transactions', 'day',
 98.1, 99.5, 'semi-automated', 'medium', 'indirect',
 'confidential', true, true, false, 'defined'),

-- Cross-Border Payment Processing
('PROC-004',
 'Cross-Border Payment Processing',
 'Complete processing of international wire transfers including FX conversion and regulatory compliance',
 'Enable secure and compliant international money transfers with competitive rates and timing',
 'Covers all international wire transfers and remittances through SWIFT and correspondent banking',
 '3.0', 'active', 5, 'International Transfers', 'high', 'high',
 4, 1, 2, 'continuous', 180, 60, 480,
 150, 500, 'transfers', 'day',
 88.5, 92.0, 'semi-automated', 'high', 'direct',
 'confidential', true, true, true, 'defined'),

-- Fraud Detection Process
('PROC-005',
 'Real-time Fraud Detection',
 'AI-powered real-time analysis of transaction patterns to identify and prevent fraudulent activities',
 'Minimize financial losses from fraud while reducing false positives that impact customer experience',
 'Covers real-time fraud screening for all payment channels and transaction types',
 '2.3', 'active', 4, 'Risk Assessment', 'critical', 'high',
 8, 2, 5, 'continuous', 1, 1, 5,
 30000, 120000, 'transactions', 'hour',
 94.8, 96.5, 'ai-enhanced', 'high', 'direct',
 'confidential', true, true, false, 'managed'),

-- KYC/AML Process
('PROC-006',
 'KYC/AML Compliance',
 'Customer due diligence, sanctions screening, and ongoing monitoring for anti-money laundering',
 'Ensure regulatory compliance and prevent financial crimes through comprehensive customer screening',
 'Covers initial KYC, periodic reviews, and ongoing transaction monitoring for all customers',
 '1.5', 'active', 4, 'Regulatory Compliance', 'critical', 'high',
 5, 8, 5, 'continuous', 15, 5, 60,
 500, 1200, 'screenings', 'day',
 96.5, 99.0, 'semi-automated', 'medium', 'indirect',
 'restricted', true, true, false, 'defined');

-- =====================================================
-- Process Steps
-- =====================================================

-- Customer Onboarding Steps
INSERT INTO process_steps (process_id, step_number, step_name, description, responsible_stakeholder_id, average_duration_minutes, is_decision_point, is_quality_gate, automation_potential) VALUES
(1, 1, 'Application Submission', 'Customer submits online or paper application with required documentation', 6, 5, false, false, 'high'),
(1, 2, 'Initial Data Validation', 'System validates completeness and format of application data', 6, 2, true, true, 'high'),
(1, 3, 'Identity Verification', 'Verify customer identity using government ID and biometric checks', 6, 15, true, true, 'medium'),
(1, 4, 'Risk Assessment', 'Evaluate customer risk profile using internal and external data sources', 8, 10, true, true, 'medium'),
(1, 5, 'Compliance Screening', 'Screen against sanctions lists and PEP databases', 5, 8, true, true, 'high'),
(1, 6, 'Account Provisioning', 'Create customer account and generate access credentials', 6, 3, false, true, 'high'),
(1, 7, 'Welcome Communication', 'Send welcome package and account activation instructions', 6, 2, false, false, 'high');

-- Payment Authorization Steps
INSERT INTO process_steps (process_id, step_number, step_name, description, responsible_stakeholder_id, average_duration_minutes, is_decision_point, is_quality_gate, automation_potential) VALUES
(2, 1, 'Request Reception', 'Receive and parse payment authorization request from merchant', 7, 0, false, false, 'high'),
(2, 2, 'Fraud Screening', 'Real-time fraud analysis using ML models and rule engine', 8, 0, true, true, 'high'),
(2, 3, 'Risk Evaluation', 'Assess transaction risk based on customer profile and behavior', 8, 0, true, true, 'high'),
(2, 4, 'Network Authorization', 'Route request to card network for approval', 7, 1, true, true, 'high'),
(2, 5, 'Response Processing', 'Process network response and format merchant response', 7, 0, false, false, 'high');

-- Settlement Reconciliation Steps
INSERT INTO process_steps (process_id, step_number, step_name, description, responsible_stakeholder_id, average_duration_minutes, is_decision_point, is_quality_gate, automation_potential) VALUES
(3, 1, 'Data Collection', 'Collect settlement files from all payment networks', 9, 30, false, true, 'high'),
(3, 2, 'Transaction Matching', 'Match internal transactions with network settlement records', 9, 60, true, true, 'high'),
(3, 3, 'Exception Investigation', 'Research and resolve unmatched or disputed items', 9, 25, true, false, 'low'),
(3, 4, 'Financial Posting', 'Post reconciled amounts to general ledger', 9, 5, false, true, 'medium');

-- =====================================================
-- Process Relationships
-- =====================================================

INSERT INTO process_relationships (parent_process_id, child_process_id, relationship_type, sequence_order, dependency_type, criticality, description) VALUES
(1, 6, 'triggers', 1, 'hard', 'critical', 'Customer onboarding triggers KYC/AML screening'),
(2, 5, 'triggers', 1, 'hard', 'critical', 'Payment authorization triggers fraud detection'),
(2, 3, 'provides-input', 2, 'hard', 'important', 'Authorized payments feed into reconciliation process'),
(4, 6, 'triggers', 1, 'hard', 'critical', 'Cross-border payments trigger enhanced KYC/AML screening'),
(4, 3, 'provides-input', 2, 'hard', 'important', 'International transfers feed into reconciliation');

-- =====================================================
-- Process-System Relationships
-- =====================================================

INSERT INTO process_systems (process_id, system_id, system_role, criticality, usage_description, is_single_point_of_failure) VALUES
-- Customer Onboarding Systems
(1, 1, 'primary', 'critical', 'Customer data storage and case management', true),
(1, 5, 'integration', 'critical', 'Identity document verification and biometric matching', false),
(1, 3, 'integration', 'important', 'Risk scoring and fraud detection', false),
(1, 8, 'supporting', 'medium', 'Customer notifications and communications', false),

-- Payment Authorization Systems
(2, 2, 'primary', 'critical', 'Core payment processing and routing engine', true),
(2, 3, 'integration', 'critical', 'Real-time fraud detection and risk scoring', false),

-- Settlement Reconciliation Systems
(3, 7, 'primary', 'critical', 'Automated matching and exception management', false),
(3, 4, 'integration', 'critical', 'Financial posting and accounting integration', true),
(3, 2, 'secondary', 'important', 'Source of internal transaction data', false),

-- Cross-Border Processing Systems
(4, 6, 'primary', 'critical', 'SWIFT messaging and international settlement', true),
(4, 2, 'integration', 'important', 'Payment initiation and status tracking', false),
(4, 3, 'integration', 'important', 'Enhanced fraud screening for international transfers', false),

-- Fraud Detection Systems
(5, 3, 'primary', 'critical', 'ML-based fraud detection and rule engine', true),
(5, 2, 'integration', 'critical', 'Transaction data and authorization interface', false),

-- KYC/AML Systems
(6, 1, 'primary', 'important', 'Customer data and screening case management', false),
(6, 3, 'integration', 'important', 'Risk profiling and behavioral analysis', false),
(6, 5, 'integration', 'critical', 'Identity verification and document checks', false);

-- =====================================================
-- Process Stakeholders (RACI)
-- =====================================================

INSERT INTO process_stakeholders (process_id, stakeholder_id, role_type, raci, responsibility_description, involvement_frequency, time_investment_hours_per_week, authority_level) VALUES
-- Customer Onboarding Stakeholders
(1, 1, 'owner', 'A', 'Overall process performance and customer experience', 'daily', 20.0, 'Manager - Process changes and escalations'),
(1, 6, 'participant', 'R', 'Daily execution of onboarding activities', 'daily', 40.0, 'Individual cases and standard procedures'),
(1, 5, 'reviewer', 'C', 'Compliance review and regulatory guidance', 'weekly', 5.0, 'Compliance decisions and policy interpretation'),
(1, 8, 'participant', 'C', 'Risk assessment and fraud prevention input', 'daily', 10.0, 'Risk scoring parameters and case recommendations'),

-- Payment Authorization Stakeholders  
(2, 2, 'owner', 'A', 'System performance and authorization strategy', 'daily', 25.0, 'System configuration and performance targets'),
(2, 7, 'participant', 'R', 'System monitoring and technical operations', 'daily', 40.0, 'Technical troubleshooting and system maintenance'),
(2, 8, 'participant', 'R', 'Fraud rule configuration and model tuning', 'daily', 15.0, 'Risk parameters and fraud detection thresholds'),

-- Settlement Reconciliation Stakeholders
(3, 3, 'owner', 'A', 'Reconciliation accuracy and financial controls', 'daily', 30.0, 'Process improvements and exception resolution'),
(3, 9, 'participant', 'R', 'Daily reconciliation execution and exception handling', 'daily', 35.0, 'Individual reconciliation decisions and research'),
(3, 10, 'reviewer', 'C', 'Treasury impact and cash positioning', 'daily', 10.0, 'Treasury and liquidity management decisions'),

-- Cross-Border Processing Stakeholders
(4, 4, 'owner', 'A', 'International operations and correspondent relationships', 'daily', 25.0, 'Operational changes and relationship management'),
(4, 1, 'reviewer', 'C', 'Customer experience and service level oversight', 'weekly', 5.0, 'Customer escalations and service improvements'),
(4, 5, 'participant', 'R', 'Regulatory compliance and sanctions screening', 'daily', 15.0, 'Compliance holds and regulatory interpretation'),

-- Fraud Detection Stakeholders
(5, 8, 'owner', 'A', 'Fraud model performance and strategy', 'daily', 30.0, 'Model parameters and fraud strategy'),
(5, 2, 'reviewer', 'C', 'System integration and performance impact', 'weekly', 8.0, 'System performance and integration decisions'),
(5, 7, 'participant', 'I', 'Technical implementation and monitoring', 'daily', 5.0, 'Technical alerts and system status'),

-- KYC/AML Stakeholders
(6, 5, 'owner', 'A', 'Compliance program effectiveness and regulatory adherence', 'daily', 35.0, 'Compliance strategy and regulatory decisions'),
(6, 8, 'participant', 'R', 'Daily screening execution and case investigation', 'daily', 25.0, 'Individual screening decisions and case research'),
(6, 1, 'reviewer', 'C', 'Customer impact and operational efficiency', 'weekly', 3.0, 'Customer experience balance with compliance');

-- =====================================================
-- Performance Metrics and KPIs
-- =====================================================

INSERT INTO process_kpis (process_id, kpi_name, description, measurement_method, current_value, target_value, unit_of_measure, measurement_frequency, owner_stakeholder_id) VALUES
-- Customer Onboarding KPIs
(1, 'Processing Time', 'Average time from application to account activation', 'Time difference between application submission and account activation', '42 minutes', '30 minutes', 'minutes', 'daily', 1),
(1, 'Success Rate', 'Percentage of applications successfully processed to completion', 'Completed applications / Total applications * 100', '95.2%', '98.0%', 'percentage', 'daily', 1),
(1, 'Customer Satisfaction', 'Post-onboarding customer satisfaction score', 'Survey responses on 5-point scale', '4.2', '4.5', 'score', 'weekly', 1),
(1, 'Manual Review Rate', 'Percentage of applications requiring manual review', 'Manual reviews / Total applications * 100', '15.3%', '10.0%', 'percentage', 'daily', 6),

-- Payment Authorization KPIs
(2, 'Authorization Rate', 'Percentage of valid transactions approved', 'Approved transactions / Valid transaction requests * 100', '92.3%', '95.0%', 'percentage', 'real-time', 2),
(2, 'Response Time', 'Average time to respond to authorization requests', 'Time difference between request receipt and response', '1.8 seconds', '1.5 seconds', 'seconds', 'real-time', 2),
(2, 'System Availability', 'Payment system uptime percentage', 'Available time / Total time * 100', '99.97%', '99.99%', 'percentage', 'daily', 2),
(2, 'False Positive Rate', 'Legitimate transactions incorrectly declined as fraud', 'False fraud declines / Total legitimate transactions * 100', '2.1%', '1.5%', 'percentage', 'daily', 8),

-- Settlement Reconciliation KPIs
(3, 'Match Rate', 'Percentage of transactions automatically matched', 'Auto-matched transactions / Total transactions * 100', '98.1%', '99.5%', 'percentage', 'daily', 3),
(3, 'Exception Resolution Time', 'Average time to resolve unmatched items', 'Time difference between exception identification and resolution', '2.5 hours', '2.0 hours', 'hours', 'daily', 9),
(3, 'Reconciliation Completion Time', 'Time to complete daily reconciliation process', 'Time from start to final posting', '105 minutes', '90 minutes', 'minutes', 'daily', 3),

-- Cross-Border Processing KPIs
(4, 'Processing Success Rate', 'Percentage of international transfers successfully completed', 'Completed transfers / Total transfer requests * 100', '88.5%', '92.0%', 'percentage', 'daily', 4),
(4, 'Average Processing Time', 'Mean time from initiation to completion', 'Time difference between initiation and final settlement', '2.8 days', '2.0 days', 'days', 'daily', 4),
(4, 'Compliance Hold Rate', 'Percentage of transfers held for compliance review', 'Compliance holds / Total transfers * 100', '8.2%', '6.0%', 'percentage', 'daily', 5),

-- Fraud Detection KPIs  
(5, 'Fraud Detection Rate', 'Percentage of actual fraud cases detected', 'Detected fraud cases / Total fraud cases * 100', '94.8%', '96.5%', 'percentage', 'daily', 8),
(5, 'False Positive Rate', 'Legitimate transactions flagged as fraud', 'False positives / Total legitimate transactions * 100', '2.1%', '1.5%', 'percentage', 'daily', 8),
(5, 'Model Accuracy', 'Overall accuracy of fraud detection models', 'Correct predictions / Total predictions * 100', '96.2%', '97.5%', 'percentage', 'weekly', 8),

-- KYC/AML KPIs
(6, 'Screening Completion Rate', 'Percentage of required screenings completed on time', 'On-time screenings / Total required screenings * 100', '96.5%', '99.0%', 'percentage', 'daily', 5),
(6, 'Average Screening Time', 'Mean time to complete customer screening', 'Time from screening initiation to completion', '12 minutes', '10 minutes', 'minutes', 'daily', 8),
(6, 'Hit Rate', 'Percentage of screenings that identify potential issues', 'Screenings with hits / Total screenings * 100', '3.2%', '3.0%', 'percentage', 'weekly', 5);

-- =====================================================
-- SLA Definitions
-- =====================================================

INSERT INTO process_slas (process_id, metric_name, target_value, measurement_method, escalation_procedure, penalty_description) VALUES
(1, 'Application Processing Time', '< 2 hours', 'Time from complete application to account activation', 'Escalate to VP Customer Operations after 3 hours', 'Customer compensation for delays > 4 hours'),
(1, 'Identity Verification Success Rate', '> 95%', 'Successful verifications / Total verification attempts', 'Daily review if rate falls below 93%', 'Additional manual review resources required'),

(2, 'Authorization Response Time', '< 3 seconds', 'Time from request receipt to response transmission', 'Immediate escalation if > 5 seconds', 'Network fines for sustained poor performance'),
(2, 'System Availability', '99.95%', 'Available time / Total time over monthly period', 'Emergency response for any outage > 5 minutes', 'Revenue impact compensation'),

(3, 'Daily Reconciliation Completion', 'Before 6 AM next business day', 'Timestamp of final reconciliation posting', 'Escalate to CFO if not complete by 8 AM', 'Delayed financial reporting'),
(3, 'Exception Resolution', '< 4 hours', 'Time from exception identification to resolution', 'Manager review for exceptions > 6 hours', 'Potential regulatory reporting delays'),

(4, 'Cross-Border Processing', '< 3 business days', 'Time from initiation to beneficiary credit', 'Daily review of items > 2 days', 'Customer compensation for delays > 5 days'),
(4, 'Compliance Screening', '< 30 minutes', 'Time to complete regulatory screening', 'Immediate review for screening > 1 hour', 'Potential regulatory violations');

-- =====================================================
-- Risk Assessment Data
-- =====================================================

INSERT INTO process_risks (process_id, risk_name, description, risk_category, probability, impact, mitigation_strategy, mitigation_owner_stakeholder_id, status) VALUES
-- Customer Onboarding Risks
(1, 'Identity Fraud', 'Risk of fraudulent identity documents or synthetic identities', 'Fraud Risk', 'medium', 'high', 'Multi-source identity verification, biometric matching, and behavioral analysis', 8, 'mitigating'),
(1, 'Regulatory Non-Compliance', 'Risk of failing to meet KYC/AML requirements', 'Compliance Risk', 'low', 'very-high', 'Comprehensive compliance training, automated screening, and regular audits', 5, 'monitoring'),
(1, 'System Outage', 'CRM or verification system unavailability', 'Operational Risk', 'low', 'high', 'Redundant systems, disaster recovery procedures, and manual backup processes', 2, 'monitoring'),

-- Payment Authorization Risks
(2, 'System Failure', 'Core payment system outage or degraded performance', 'Operational Risk', 'low', 'very-high', 'Multi-region deployment, automatic failover, and real-time monitoring', 2, 'mitigating'),
(2, 'Fraud Losses', 'Financial losses from undetected fraudulent transactions', 'Fraud Risk', 'medium', 'high', 'Advanced ML models, real-time pattern analysis, and consortium data sharing', 8, 'mitigating'),
(2, 'Network Connectivity', 'Loss of connection to card networks', 'Technical Risk', 'medium', 'high', 'Multiple network connections, cached authorization, and offline procedures', 7, 'monitoring'),

-- Settlement Reconciliation Risks
(3, 'Reconciliation Errors', 'Incorrect matching leading to financial misstatements', 'Operational Risk', 'medium', 'medium', 'Automated validation rules, exception reporting, and supervisory review', 9, 'monitoring'),
(3, 'Data Quality Issues', 'Incomplete or corrupted settlement data', 'Data Risk', 'medium', 'medium', 'Data validation checks, source system monitoring, and backup data sources', 3, 'mitigating'),

-- Cross-Border Processing Risks
(4, 'Sanctions Violations', 'Risk of processing payments to sanctioned entities', 'Compliance Risk', 'low', 'very-high', 'Real-time sanctions screening, enhanced due diligence, and regular list updates', 5, 'mitigating'),
(4, 'Correspondent Bank Issues', 'Problems with correspondent banking relationships', 'Operational Risk', 'medium', 'high', 'Multiple correspondent relationships, regular due diligence, and alternative routing', 4, 'monitoring'),
(4, 'Foreign Exchange Risk', 'Currency rate fluctuations impacting profitability', 'Financial Risk', 'high', 'medium', 'Real-time rate updates, hedging strategies, and rate monitoring', 10, 'mitigating'),

-- Fraud Detection Risks
(5, 'Model Degradation', 'Fraud detection models becoming less effective over time', 'Model Risk', 'medium', 'high', 'Regular model retraining, performance monitoring, and challenger models', 8, 'mitigating'),
(5, 'False Positives', 'Legitimate transactions incorrectly blocked as fraud', 'Customer Risk', 'medium', 'medium', 'Model tuning, feedback loops, and customer authentication options', 8, 'monitoring'),

-- KYC/AML Risks
(6, 'Regulatory Changes', 'New or changing compliance requirements', 'Regulatory Risk', 'high', 'high', 'Regulatory monitoring, legal counsel, and agile compliance procedures', 5, 'monitoring'),
(6, 'Screening Failures', 'Missing or incorrect identification of high-risk customers', 'Compliance Risk', 'low', 'very-high', 'Comprehensive screening procedures, regular audits, and staff training', 5, 'mitigating');

-- =====================================================
-- Compliance Requirements
-- =====================================================

INSERT INTO process_compliance_requirements (process_id, requirement_name, requirement_type, regulation_name, description, compliance_status, last_assessment_date, next_assessment_date, responsible_stakeholder_id, evidence_location) VALUES
-- Customer Onboarding Compliance
(1, 'Customer Identification Program', 'regulatory', 'Bank Secrecy Act', 'Verify customer identity using government-issued identification', 'compliant', '2024-12-01', '2025-06-01', 5, '/compliance/kyc/cip-procedures'),
(1, 'Know Your Customer', 'regulatory', 'AML Requirements', 'Understand customer business and risk profile', 'compliant', '2024-12-01', '2025-06-01', 5, '/compliance/kyc/kyc-procedures'),
(1, 'Data Privacy Protection', 'regulatory', 'CCPA/GDPR', 'Protect customer personal information and privacy rights', 'compliant', '2024-11-15', '2025-05-15', 1, '/compliance/privacy/data-protection'),

-- Payment Authorization Compliance
(2, 'PCI DSS Compliance', 'industry-standard', 'PCI DSS', 'Secure handling of payment card information', 'compliant', '2024-10-01', '2025-04-01', 2, '/compliance/pci/assessment-report'),
(2, 'Network Rules Compliance', 'industry-standard', 'Visa/Mastercard Rules', 'Adherence to card network operating regulations', 'compliant', '2024-12-15', '2025-06-15', 2, '/compliance/network/rules-compliance'),

-- Settlement Reconciliation Compliance
(3, 'Financial Reporting', 'regulatory', 'SOX', 'Accurate and timely financial reporting', 'compliant', '2024-12-31', '2025-12-31', 3, '/compliance/sox/financial-controls'),
(3, 'Audit Trail Requirements', 'regulatory', 'SOX', 'Maintain complete audit trail for financial transactions', 'compliant', '2024-12-31', '2025-12-31', 3, '/compliance/sox/audit-trails'),

-- Cross-Border Processing Compliance
(4, 'OFAC Sanctions Screening', 'regulatory', 'OFAC', 'Screen all international transfers against sanctions lists', 'compliant', '2024-12-01', '2025-03-01', 5, '/compliance/sanctions/ofac-screening'),
(4, 'Anti-Money Laundering', 'regulatory', 'BSA/AML', 'Monitor and report suspicious international transactions', 'compliant', '2024-12-01', '2025-06-01', 5, '/compliance/aml/international-monitoring'),
(4, 'Travel Rule Compliance', 'regulatory', 'FATF Travel Rule', 'Include required information in international transfers', 'compliant', '2024-11-01', '2025-05-01', 5, '/compliance/travel-rule/documentation'),

-- KYC/AML Compliance
(6, 'Suspicious Activity Reporting', 'regulatory', 'BSA', 'File SARs for suspicious customer activity', 'compliant', '2024-12-01', '2025-06-01', 5, '/compliance/sar/reporting-procedures'),
(6, 'Customer Due Diligence', 'regulatory', 'CDD Rule', 'Enhanced due diligence for high-risk customers', 'compliant', '2024-12-01', '2025-06-01', 5, '/compliance/cdd/procedures');

-- =====================================================
-- Business Rules
-- =====================================================

INSERT INTO process_business_rules (process_id, rule_code, rule_name, description, condition_logic, action_description, exceptions, is_automated, priority) VALUES
-- Customer Onboarding Rules
(1, 'BR-001', 'Minimum Age Requirement', 'Customer must be 18 or older to open account', 'customer_age >= 18', 'Proceed with application processing', 'Legal guardian consent for ages 16-17', true, 1),
(1, 'BR-002', 'Identity Verification Required', 'All customers must pass identity verification', 'identity_verification_status == "PASSED"', 'Continue to risk assessment', 'Manual review for edge cases or system failures', true, 1),
(1, 'BR-003', 'Risk Score Threshold', 'Customer risk score must be below acceptable threshold', 'risk_score <= max_acceptable_score', 'Approve account opening', 'Enhanced due diligence for borderline scores', true, 2),

-- Payment Authorization Rules
(2, 'BR-004', 'Fraud Score Threshold', 'Transactions exceeding fraud threshold must be declined', 'fraud_score > decline_threshold', 'Decline transaction with fraud reason', 'Manual review for VIP customers', true, 1),
(2, 'BR-005', 'Velocity Limits', 'Enforce transaction velocity limits per customer', 'transaction_count_period <= velocity_limit', 'Approve if within limits', 'Temporary increases for pre-approved customers', true, 2),
(2, 'BR-006', 'High Value Authorization', 'Transactions over $10,000 require additional verification', 'transaction_amount > 10000', 'Require additional authentication', 'Corporate customers with pre-authorization', false, 3),

-- Settlement Reconciliation Rules
(3, 'BR-007', 'Auto-Approval Variance', 'Variances under $100 are auto-approved', 'abs(variance) < 100', 'Auto-approve and post adjustment', 'None - all small variances are acceptable', true, 2),
(3, 'BR-008', 'Daily Cutoff Time', 'Reconciliation must be completed by 6 AM', 'completion_time <= "06:00"', 'Standard processing', 'Weekend and holiday adjustments', true, 1),

-- Cross-Border Processing Rules
(4, 'BR-009', 'Enhanced Screening Threshold', 'International transfers over $3,000 require enhanced screening', 'transfer_amount > 3000', 'Perform enhanced due diligence', 'Regular customers with established pattern', true, 1),
(4, 'BR-010', 'Sanctions Screening Required', 'All international transfers must be screened against sanctions lists', 'transfer_type == "international"', 'Perform sanctions screening before processing', 'No exceptions permitted', true, 1),

-- KYC/AML Rules
(6, 'BR-011', 'Periodic Review Schedule', 'High-risk customers require annual review', 'customer_risk_level == "HIGH"', 'Schedule annual review', 'More frequent reviews for very high risk', true, 2),
(6, 'BR-012', 'SAR Filing Threshold', 'Suspicious activity over $5,000 requires SAR filing', 'suspicious_amount > 5000 AND confidence > 0.8', 'File SAR within required timeframe', 'Lower threshold for repeat offenders', false, 1);

-- =====================================================
-- Improvement Opportunities
-- =====================================================

INSERT INTO process_improvements (process_id, title, description, improvement_type, priority, status, estimated_effort, expected_benefits, success_criteria, owner_stakeholder_id, target_completion_date, investment_required, annual_savings_estimate) VALUES
-- Customer Onboarding Improvements
(1, 'Automated Document Processing', 'Implement OCR and AI for automatic document verification and data extraction', 'automation', 'high', 'planned', '3-4 months', 'Reduce processing time by 40%, improve accuracy, reduce manual effort', 'Processing time < 25 minutes, accuracy > 98%', 1, '2025-06-30', 150000, 200000),
(1, 'Real-time Risk Scoring', 'Integrate ML-based risk assessment for instant decision making', 'optimization', 'medium', 'identified', '2-3 months', 'Faster processing, better risk detection, improved customer experience', 'Risk assessment < 5 minutes, false positive rate < 5%', 8, '2025-09-30', 75000, 100000),

-- Payment Authorization Improvements
(2, 'Enhanced ML Models', 'Deploy advanced machine learning models for fraud detection', 'optimization', 'high', 'in-progress', '4-6 months', 'Reduce false positives by 30%, improve fraud detection by 15%', 'False positive rate < 1.5%, fraud detection > 96%', 8, '2025-04-30', 200000, 500000),
(2, 'Network Token Adoption', 'Implement network tokenization to improve authorization rates', 'integration', 'high', 'planned', '2-3 months', 'Increase authorization rates by 10-15%, enhance security', 'Authorization rate > 94%, reduced card declines', 2, '2025-05-31', 100000, 300000),

-- Settlement Reconciliation Improvements
(3, 'Real-time Reconciliation', 'Move from batch to real-time transaction reconciliation', 'optimization', 'medium', 'identified', '6-8 months', 'Faster exception identification, reduced end-of-day processing time', 'Exceptions identified within 1 hour, 50% reduction in batch processing time', 3, '2025-12-31', 250000, 150000),
(3, 'Automated Exception Handling', 'Implement AI for automatic resolution of common reconciliation exceptions', 'automation', 'medium', 'identified', '4-5 months', 'Reduce manual effort by 60%, faster resolution times', 'Auto-resolution rate > 80%, average resolution time < 1 hour', 9, '2025-10-31', 120000, 180000),

-- Cross-Border Processing Improvements
(4, 'Blockchain Settlement Pilot', 'Pilot blockchain-based settlement for specific corridors', 'integration', 'low', 'identified', '8-12 months', 'Reduce settlement time by 80%, lower costs, improved transparency', 'Settlement time < 4 hours, cost reduction > 25%', 4, '2026-06-30', 500000, 800000),
(4, 'API-Based Processing', 'Replace legacy SWIFT processing with modern API-based system', 'optimization', 'high', 'planned', '6-9 months', 'Faster processing, better tracking, improved customer experience', 'Processing time < 1 day, real-time status updates', 4, '2025-11-30', 300000, 400000),

-- Fraud Detection Improvements
(5, 'Behavioral Biometrics', 'Implement behavioral biometric analysis for enhanced fraud detection', 'optimization', 'medium', 'identified', '3-4 months', 'Reduce false positives, detect new fraud patterns, passive authentication', 'False positive reduction > 20%, new fraud pattern detection', 8, '2025-08-31', 180000, 250000),

-- KYC/AML Improvements
(6, 'Automated Screening Workflow', 'Implement workflow automation for routine screening tasks', 'automation', 'high', 'planned', '2-3 months', 'Reduce manual effort by 70%, consistent processing, faster completion', 'Manual effort < 30%, processing time < 8 minutes', 5, '2025-05-31', 80000, 150000);

-- =====================================================
-- Pain Points
-- =====================================================

INSERT INTO process_pain_points (process_id, title, description, category, impact_level, frequency, affected_stakeholders, root_cause, workaround, reported_by_stakeholder_id, status) VALUES
-- Customer Onboarding Pain Points
(1, 'Manual Document Review', 'Extensive manual review required for identity documents causing delays', 'Process Efficiency', 'high', 'daily', 'Customer service representatives, customers', 'Legacy system limitations and lack of OCR technology', 'Priority queuing for simple cases', 6, 'open'),
(1, 'System Integration Delays', 'Multiple system handoffs cause processing delays and potential errors', 'Technology', 'medium', 'daily', 'Operations team, IT support', 'Point-to-point integrations without proper error handling', 'Manual data entry for failed integrations', 1, 'investigating'),

-- Payment Authorization Pain Points
(2, 'Network Latency Issues', 'Occasional network latency affecting authorization response times', 'Technology', 'medium', 'weekly', 'Payment engineers, merchants, customers', 'Single network provider for certain regions', 'Automatic retry logic with exponential backoff', 7, 'open'),
(2, 'False Fraud Positives', 'Legitimate transactions being declined as fraudulent', 'Process Quality', 'high', 'daily', 'Customers, customer service, risk team', 'Overly conservative fraud models', 'Manual review queue for borderline cases', 8, 'open'),

-- Settlement Reconciliation Pain Points
(3, 'Late Settlement Files', 'Network settlement files frequently arrive late causing reconciliation delays', 'External Dependencies', 'medium', 'weekly', 'Finance team, reconciliation analysts', 'Network processing delays and different time zones', 'Extended reconciliation windows for late files', 9, 'open'),
(3, 'Complex Exception Investigation', 'Time-consuming manual research for reconciliation exceptions', 'Process Efficiency', 'medium', 'daily', 'Financial analysts', 'Limited transaction details and multiple data sources', 'Escalation to senior analysts for complex cases', 3, 'open'),

-- Cross-Border Processing Pain Points
(4, 'Correspondent Bank Delays', 'Delays in correspondent bank processing affecting customer experience', 'External Dependencies', 'high', 'weekly', 'Customers, international team', 'Limited correspondent relationships and complex routing', 'Direct relationships with major banks in key corridors', 4, 'investigating'),
(4, 'Manual Compliance Reviews', 'High percentage of international transfers requiring manual compliance review', 'Process Efficiency', 'high', 'daily', 'Compliance team, customers', 'Conservative screening parameters and limited automation', 'Dedicated compliance staff for international transfers', 5, 'open'),

-- Fraud Detection Pain Points
(5, 'Model Maintenance Overhead', 'Significant effort required to maintain and tune fraud detection models', 'Process Efficiency', 'medium', 'monthly', 'Risk analysts, data scientists', 'Complex model interactions and frequent retraining needs', 'Automated model monitoring and alerting', 8, 'open'),

-- KYC/AML Pain Points
(6, 'Regulatory Update Lag', 'Delays in implementing new regulatory requirements into screening procedures', 'Compliance', 'high', 'quarterly', 'Compliance team, operations', 'Manual process for regulatory change management', 'Enhanced monitoring during regulatory change periods', 5, 'investigating');

-- =====================================================
-- Performance History (Sample data for trends)
-- =====================================================

-- Generate sample performance data for the last 30 days
INSERT INTO process_performance_history (process_id, measurement_date, success_rate, average_duration_minutes, volume_processed, error_count, customer_satisfaction_score, notes)
SELECT 
    p.process_id,
    CURRENT_DATE - (generate_series * INTERVAL '1 day'),
    -- Simulate realistic performance variations
    p.current_success_rate + (RANDOM() * 4 - 2), -- +/- 2% variation
    p.average_duration_minutes + (RANDOM() * 10 - 5)::INTEGER, -- +/- 5 minute variation
    (p.average_volume + (RANDOM() * p.average_volume * 0.3)::INTEGER), -- +/- 30% volume variation
    (RANDOM() * 10)::INTEGER, -- 0-10 errors per day
    4.0 + (RANDOM() * 1), -- 4.0-5.0 satisfaction score
    CASE 
        WHEN RANDOM() < 0.1 THEN 'System maintenance window'
        WHEN RANDOM() < 0.05 THEN 'High volume due to marketing campaign'
        ELSE NULL
    END
FROM processes p
CROSS JOIN generate_series(0, 29) -- Last 30 days
WHERE p.status = 'active';

-- =====================================================
-- Geographic Scope
-- =====================================================

INSERT INTO process_geographic_scope (process_id, country_code, country_name, region, is_primary_location) VALUES
-- Customer Onboarding - North America focus
(1, 'US', 'United States', 'North America', true),
(1, 'CA', 'Canada', 'North America', false),
(1, 'MX', 'Mexico', 'North America', false),

-- Payment Authorization - Global
(2, 'US', 'United States', 'North America', true),
(2, 'GB', 'United Kingdom', 'Europe', false),
(2, 'DE', 'Germany', 'Europe', false),
(2, 'SG', 'Singapore', 'Asia Pacific', false),
(2, 'AU', 'Australia', 'Asia Pacific', false),

-- Settlement Reconciliation - Regional processing centers
(3, 'US', 'United States', 'North America', true),
(3, 'GB', 'United Kingdom', 'Europe', false),
(3, 'SG', 'Singapore', 'Asia Pacific', false),

-- Cross-Border Processing - Global corridors
(4, 'US', 'United States', 'North America', true),
(4, 'GB', 'United Kingdom', 'Europe', false),
(4, 'DE', 'Germany', 'Europe', false),
(4, 'FR', 'France', 'Europe', false),
(4, 'JP', 'Japan', 'Asia Pacific', false),
(4, 'SG', 'Singapore', 'Asia Pacific', false),
(4, 'AU', 'Australia', 'Asia Pacific', false),
(4, 'BR', 'Brazil', 'Latin America', false),
(4, 'MX', 'Mexico', 'Latin America', false),

-- Fraud Detection - Global coverage
(5, 'US', 'United States', 'North America', true),
(5, 'GB', 'United Kingdom', 'Europe', false),
(5, 'DE', 'Germany', 'Europe', false),
(5, 'SG', 'Singapore', 'Asia Pacific', false),

-- KYC/AML - Regulatory jurisdictions
(6, 'US', 'United States', 'North America', true),
(6, 'GB', 'United Kingdom', 'Europe', false),
(6, 'DE', 'Germany', 'Europe', false),
(6, 'SG', 'Singapore', 'Asia Pacific', false);

-- =====================================================
-- Process Reviews
-- =====================================================

INSERT INTO process_reviews (process_id, review_type, reviewer_stakeholder_id, review_date, review_status, findings, recommendations, next_review_date) VALUES
(1, 'regular', 1, '2024-12-01', 'completed', 'Process performing well overall, some opportunities for automation', 'Implement OCR for document processing, consider API integrations', '2025-06-01'),
(2, 'audit', 2, '2024-11-15', 'completed', 'Strong technical controls, minor gaps in monitoring', 'Enhanced real-time alerting, update runbooks', '2025-05-15'),
(3, 'regular', 3, '2024-12-15', 'completed', 'Good accuracy but manual effort is high', 'Investigate automation opportunities for common exceptions', '2025-06-15'),
(4, 'change-control', 4, '2024-12-20', 'approved', 'New API integration ready for implementation', 'Proceed with phased rollout starting Q2 2025', '2025-03-20'),
(5, 'improvement', 8, '2024-11-30', 'completed', 'Model performance is good but can be optimized', 'Implement ensemble models and feature engineering', '2025-05-30'),
(6, 'regular', 5, '2024-12-10', 'completed', 'Compliance procedures are robust and up to date', 'Continue current procedures, monitor for regulatory changes', '2025-06-10');