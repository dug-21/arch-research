-- Business Process Inventory Database Schema
-- This schema supports comprehensive process documentation and analysis
-- Designed for PostgreSQL but adaptable to other RDBMS

-- =====================================================
-- Core Entity Tables
-- =====================================================

-- Organizations and Business Units
CREATE TABLE organizations (
    organization_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    parent_organization_id INTEGER REFERENCES organizations(organization_id),
    organization_type VARCHAR(50) CHECK (organization_type IN ('enterprise', 'division', 'department', 'team')),
    description TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, parent_organization_id)
);

-- Process Categories
CREATE TABLE process_categories (
    category_id SERIAL PRIMARY KEY,
    category_code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    parent_category_id INTEGER REFERENCES process_categories(category_id),
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- System/Application Inventory
CREATE TABLE systems (
    system_id SERIAL PRIMARY KEY,
    system_code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    system_type VARCHAR(50) CHECK (system_type IN ('core', 'supporting', 'integration', 'reporting', 'external')),
    vendor VARCHAR(100),
    version VARCHAR(50),
    status VARCHAR(20) CHECK (status IN ('production', 'development', 'testing', 'deprecated', 'retired')) DEFAULT 'production',
    criticality VARCHAR(20) CHECK (criticality IN ('critical', 'high', 'medium', 'low')),
    owner_contact VARCHAR(100),
    support_contact VARCHAR(100),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Stakeholder Directory
CREATE TABLE stakeholders (
    stakeholder_id SERIAL PRIMARY KEY,
    employee_id VARCHAR(50) UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(200) UNIQUE,
    phone VARCHAR(50),
    title VARCHAR(200),
    department VARCHAR(200),
    organization_id INTEGER REFERENCES organizations(organization_id),
    manager_stakeholder_id INTEGER REFERENCES stakeholders(stakeholder_id),
    is_active BOOLEAN DEFAULT true,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Process Core Tables
-- =====================================================

-- Main Process Inventory
CREATE TABLE processes (
    process_id SERIAL PRIMARY KEY,
    process_code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    purpose TEXT,
    scope_description TEXT,
    version VARCHAR(20) DEFAULT '1.0',
    status VARCHAR(20) CHECK (status IN ('active', 'deprecated', 'planned', 'suspended', 'retired')) DEFAULT 'active',
    
    -- Classification
    category_id INTEGER REFERENCES process_categories(category_id),
    sub_category VARCHAR(100),
    business_priority VARCHAR(20) CHECK (business_priority IN ('critical', 'high', 'medium', 'low')),
    risk_level VARCHAR(20) CHECK (risk_level IN ('very-low', 'low', 'medium', 'high', 'very-high')),
    
    -- Ownership
    owner_stakeholder_id INTEGER REFERENCES stakeholders(stakeholder_id),
    backup_owner_stakeholder_id INTEGER REFERENCES stakeholders(stakeholder_id),
    organization_id INTEGER REFERENCES organizations(organization_id),
    
    -- Operational Details
    frequency VARCHAR(50) CHECK (frequency IN ('continuous', 'real-time', 'hourly', 'daily', 'weekly', 'monthly', 'quarterly', 'annually', 'ad-hoc', 'event-driven')),
    average_duration_minutes INTEGER,
    min_duration_minutes INTEGER,
    max_duration_minutes INTEGER,
    
    -- Volume Information
    average_volume INTEGER,
    peak_volume INTEGER,
    volume_unit VARCHAR(50),
    volume_period VARCHAR(20) CHECK (volume_period IN ('hour', 'day', 'week', 'month')),
    
    -- Performance
    current_success_rate DECIMAL(5,2) CHECK (current_success_rate >= 0 AND current_success_rate <= 100),
    target_success_rate DECIMAL(5,2) CHECK (target_success_rate >= 0 AND target_success_rate <= 100),
    
    -- Technical Details
    automation_level VARCHAR(20) CHECK (automation_level IN ('manual', 'semi-automated', 'fully-automated', 'ai-enhanced')),
    
    -- Business Context
    customer_impact VARCHAR(20) CHECK (customer_impact IN ('critical', 'high', 'medium', 'low', 'none')),
    revenue_impact VARCHAR(20) CHECK (revenue_impact IN ('direct', 'indirect', 'cost-center', 'none')),
    
    -- Compliance and Security
    security_classification VARCHAR(20) CHECK (security_classification IN ('public', 'internal', 'confidential', 'restricted', 'top-secret')),
    is_regulatory_required BOOLEAN DEFAULT false,
    is_audit_trail_required BOOLEAN DEFAULT false,
    
    -- Seasonal and Geographic
    has_seasonal_variation BOOLEAN DEFAULT false,
    
    -- Quality and Documentation
    documentation_quality_score INTEGER CHECK (documentation_quality_score >= 0 AND documentation_quality_score <= 100),
    process_maturity_level VARCHAR(20) CHECK (process_maturity_level IN ('initial', 'developing', 'defined', 'managed', 'optimized')),
    
    -- Timestamps
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_reviewed_date TIMESTAMP,
    next_review_date TIMESTAMP
);

-- Process Steps/Activities
CREATE TABLE process_steps (
    step_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    step_number INTEGER NOT NULL,
    step_name VARCHAR(200) NOT NULL,
    description TEXT,
    responsible_stakeholder_id INTEGER REFERENCES stakeholders(stakeholder_id),
    average_duration_minutes INTEGER,
    is_decision_point BOOLEAN DEFAULT false,
    is_quality_gate BOOLEAN DEFAULT false,
    automation_potential VARCHAR(20) CHECK (automation_potential IN ('high', 'medium', 'low', 'none')),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(process_id, step_number)
);

-- =====================================================
-- Relationship Tables
-- =====================================================

-- Process Hierarchies (Parent-Child relationships)
CREATE TABLE process_relationships (
    relationship_id SERIAL PRIMARY KEY,
    parent_process_id INTEGER REFERENCES processes(process_id),
    child_process_id INTEGER REFERENCES processes(process_id),
    relationship_type VARCHAR(50) CHECK (relationship_type IN ('parent-child', 'triggers', 'provides-input', 'prerequisite', 'depends-on')),
    sequence_order INTEGER,
    dependency_type VARCHAR(20) CHECK (dependency_type IN ('hard', 'soft', 'optional')),
    criticality VARCHAR(20) CHECK (criticality IN ('critical', 'important', 'optional')),
    description TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(parent_process_id, child_process_id, relationship_type)
);

-- Process-System Relationships
CREATE TABLE process_systems (
    process_system_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    system_id INTEGER REFERENCES systems(system_id),
    system_role VARCHAR(50) CHECK (system_role IN ('primary', 'secondary', 'integration', 'reporting', 'backup')),
    criticality VARCHAR(20) CHECK (criticality IN ('critical', 'important', 'supporting')),
    usage_description TEXT,
    is_single_point_of_failure BOOLEAN DEFAULT false,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(process_id, system_id)
);

-- Process-Stakeholder Relationships (RACI)
CREATE TABLE process_stakeholders (
    process_stakeholder_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    stakeholder_id INTEGER REFERENCES stakeholders(stakeholder_id),
    role_type VARCHAR(50) CHECK (role_type IN ('owner', 'participant', 'approver', 'reviewer', 'observer', 'informed')),
    raci VARCHAR(1) CHECK (raci IN ('R', 'A', 'C', 'I')),
    responsibility_description TEXT,
    involvement_frequency VARCHAR(50) CHECK (involvement_frequency IN ('continuous', 'daily', 'weekly', 'monthly', 'quarterly', 'as-needed')),
    time_investment_hours_per_week DECIMAL(4,1),
    authority_level VARCHAR(50),
    escalation_path TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(process_id, stakeholder_id)
);

-- Geographic Scope
CREATE TABLE process_geographic_scope (
    scope_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    country_code VARCHAR(3),
    country_name VARCHAR(100),
    region VARCHAR(100),
    is_primary_location BOOLEAN DEFAULT false,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Performance and Metrics Tables
-- =====================================================

-- Key Performance Indicators
CREATE TABLE process_kpis (
    kpi_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    kpi_name VARCHAR(200) NOT NULL,
    description TEXT,
    measurement_method TEXT,
    current_value VARCHAR(100),
    target_value VARCHAR(100),
    unit_of_measure VARCHAR(50),
    measurement_frequency VARCHAR(50),
    owner_stakeholder_id INTEGER REFERENCES stakeholders(stakeholder_id),
    is_active BOOLEAN DEFAULT true,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Service Level Agreements
CREATE TABLE process_slas (
    sla_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    metric_name VARCHAR(200) NOT NULL,
    target_value VARCHAR(100) NOT NULL,
    measurement_method TEXT,
    escalation_procedure TEXT,
    penalty_description TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Historical Performance Data
CREATE TABLE process_performance_history (
    performance_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    measurement_date DATE NOT NULL,
    success_rate DECIMAL(5,2),
    average_duration_minutes INTEGER,
    volume_processed INTEGER,
    error_count INTEGER,
    customer_satisfaction_score DECIMAL(3,2),
    cost_per_transaction DECIMAL(10,2),
    notes TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Risk and Compliance Tables
-- =====================================================

-- Risk Factors
CREATE TABLE process_risks (
    risk_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    risk_name VARCHAR(200) NOT NULL,
    description TEXT,
    risk_category VARCHAR(100),
    probability VARCHAR(20) CHECK (probability IN ('very-low', 'low', 'medium', 'high', 'very-high')),
    impact VARCHAR(20) CHECK (impact IN ('very-low', 'low', 'medium', 'high', 'very-high')),
    risk_score INTEGER GENERATED ALWAYS AS (
        CASE probability
            WHEN 'very-low' THEN 1 WHEN 'low' THEN 2 WHEN 'medium' THEN 3 
            WHEN 'high' THEN 4 WHEN 'very-high' THEN 5
        END *
        CASE impact
            WHEN 'very-low' THEN 1 WHEN 'low' THEN 2 WHEN 'medium' THEN 3 
            WHEN 'high' THEN 4 WHEN 'very-high' THEN 5
        END
    ) STORED,
    mitigation_strategy TEXT,
    mitigation_owner_stakeholder_id INTEGER REFERENCES stakeholders(stakeholder_id),
    status VARCHAR(20) CHECK (status IN ('identified', 'analyzing', 'mitigating', 'monitoring', 'closed')),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Compliance Requirements
CREATE TABLE process_compliance_requirements (
    compliance_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    requirement_name VARCHAR(200) NOT NULL,
    requirement_type VARCHAR(50) CHECK (requirement_type IN ('regulatory', 'internal-policy', 'industry-standard', 'audit')),
    regulation_name VARCHAR(200),
    description TEXT,
    compliance_status VARCHAR(20) CHECK (compliance_status IN ('compliant', 'partial', 'non-compliant', 'not-applicable')),
    last_assessment_date DATE,
    next_assessment_date DATE,
    responsible_stakeholder_id INTEGER REFERENCES stakeholders(stakeholder_id),
    evidence_location TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Business Rules and Logic Tables
-- =====================================================

-- Business Rules
CREATE TABLE process_business_rules (
    rule_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    rule_code VARCHAR(50),
    rule_name VARCHAR(200) NOT NULL,
    description TEXT,
    condition_logic TEXT,
    action_description TEXT,
    exceptions TEXT,
    is_automated BOOLEAN DEFAULT false,
    priority INTEGER DEFAULT 0,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exception Handling
CREATE TABLE process_exceptions (
    exception_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    exception_name VARCHAR(200) NOT NULL,
    description TEXT,
    trigger_conditions TEXT,
    resolution_procedure TEXT,
    escalation_procedure TEXT,
    prevention_measures TEXT,
    frequency_rating VARCHAR(20) CHECK (frequency_rating IN ('very-rare', 'rare', 'occasional', 'frequent', 'very-frequent')),
    impact_rating VARCHAR(20) CHECK (impact_rating IN ('minimal', 'minor', 'moderate', 'major', 'critical')),
    average_resolution_time_hours DECIMAL(6,2),
    responsible_stakeholder_id INTEGER REFERENCES stakeholders(stakeholder_id),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Data Flow Tables
-- =====================================================

-- Data Sources (Inputs)
CREATE TABLE process_data_inputs (
    input_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    input_name VARCHAR(200) NOT NULL,
    description TEXT,
    data_type VARCHAR(50) CHECK (data_type IN ('form', 'file', 'api', 'database', 'manual-entry', 'system-generated')),
    source_system_id INTEGER REFERENCES systems(system_id),
    source_description VARCHAR(500),
    format VARCHAR(100),
    frequency VARCHAR(50),
    volume_estimate VARCHAR(100),
    quality_requirements TEXT,
    is_required BOOLEAN DEFAULT true,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Data Outputs
CREATE TABLE process_data_outputs (
    output_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    output_name VARCHAR(200) NOT NULL,
    description TEXT,
    output_type VARCHAR(50) CHECK (output_type IN ('report', 'file', 'api-response', 'database-update', 'notification', 'transaction')),
    destination_system_id INTEGER REFERENCES systems(system_id),
    destination_description VARCHAR(500),
    format VARCHAR(100),
    frequency VARCHAR(50),
    volume_estimate VARCHAR(100),
    retention_period VARCHAR(100),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Integration Points
CREATE TABLE process_integrations (
    integration_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    integration_name VARCHAR(200) NOT NULL,
    integration_type VARCHAR(50) CHECK (integration_type IN ('api', 'file', 'database', 'message-queue', 'webhook', 'batch', 'real-time')),
    connected_system_id INTEGER REFERENCES systems(system_id),
    direction VARCHAR(20) CHECK (direction IN ('inbound', 'outbound', 'bidirectional')),
    frequency VARCHAR(50),
    data_format VARCHAR(100),
    authentication_method VARCHAR(100),
    is_critical BOOLEAN DEFAULT false,
    error_handling TEXT,
    monitoring_requirements TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Improvement and Change Management Tables
-- =====================================================

-- Improvement Opportunities
CREATE TABLE process_improvements (
    improvement_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    improvement_type VARCHAR(50) CHECK (improvement_type IN ('automation', 'optimization', 'integration', 'elimination', 'standardization')),
    priority VARCHAR(20) CHECK (priority IN ('critical', 'high', 'medium', 'low')),
    status VARCHAR(20) CHECK (status IN ('identified', 'planned', 'in-progress', 'completed', 'cancelled', 'on-hold')),
    estimated_effort VARCHAR(100),
    expected_benefits TEXT,
    success_criteria TEXT,
    owner_stakeholder_id INTEGER REFERENCES stakeholders(stakeholder_id),
    target_completion_date DATE,
    actual_completion_date DATE,
    investment_required DECIMAL(12,2),
    annual_savings_estimate DECIMAL(12,2),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pain Points and Issues
CREATE TABLE process_pain_points (
    pain_point_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    impact_level VARCHAR(20) CHECK (impact_level IN ('critical', 'high', 'medium', 'low')),
    frequency VARCHAR(20) CHECK (frequency IN ('constant', 'daily', 'weekly', 'monthly', 'occasional')),
    affected_stakeholders TEXT,
    root_cause TEXT,
    workaround TEXT,
    reported_by_stakeholder_id INTEGER REFERENCES stakeholders(stakeholder_id),
    assigned_to_stakeholder_id INTEGER REFERENCES stakeholders(stakeholder_id),
    status VARCHAR(20) CHECK (status IN ('open', 'investigating', 'resolved', 'closed', 'wont-fix')),
    resolution_description TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Audit and Version Control Tables
-- =====================================================

-- Process Audit Log
CREATE TABLE process_audit_log (
    audit_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id),
    table_name VARCHAR(100) NOT NULL,
    action VARCHAR(20) CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')) NOT NULL,
    old_values JSONB,
    new_values JSONB,
    changed_fields TEXT[],
    changed_by_stakeholder_id INTEGER REFERENCES stakeholders(stakeholder_id),
    change_reason TEXT,
    change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(100)
);

-- Process Reviews and Approvals
CREATE TABLE process_reviews (
    review_id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES processes(process_id) ON DELETE CASCADE,
    review_type VARCHAR(50) CHECK (review_type IN ('regular', 'change-control', 'audit', 'improvement')),
    reviewer_stakeholder_id INTEGER REFERENCES stakeholders(stakeholder_id),
    review_date DATE NOT NULL,
    review_status VARCHAR(20) CHECK (review_status IN ('pending', 'in-progress', 'completed', 'approved', 'rejected')),
    findings TEXT,
    recommendations TEXT,
    action_items TEXT,
    next_review_date DATE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Indices for Performance
-- =====================================================

-- Core process indices
CREATE INDEX idx_processes_status ON processes(status);
CREATE INDEX idx_processes_category ON processes(category_id);
CREATE INDEX idx_processes_owner ON processes(owner_stakeholder_id);
CREATE INDEX idx_processes_organization ON processes(organization_id);
CREATE INDEX idx_processes_priority ON processes(business_priority);
CREATE INDEX idx_processes_risk_level ON processes(risk_level);
CREATE INDEX idx_processes_updated ON processes(updated_date);

-- Relationship indices
CREATE INDEX idx_process_relationships_parent ON process_relationships(parent_process_id);
CREATE INDEX idx_process_relationships_child ON process_relationships(child_process_id);
CREATE INDEX idx_process_systems_process ON process_systems(process_id);
CREATE INDEX idx_process_systems_system ON process_systems(system_id);
CREATE INDEX idx_process_stakeholders_process ON process_stakeholders(process_id);
CREATE INDEX idx_process_stakeholders_stakeholder ON process_stakeholders(stakeholder_id);

-- Performance indices
CREATE INDEX idx_process_performance_date ON process_performance_history(measurement_date);
CREATE INDEX idx_process_performance_process ON process_performance_history(process_id);

-- Risk and compliance indices
CREATE INDEX idx_process_risks_level ON process_risks(risk_score DESC);
CREATE INDEX idx_process_compliance_status ON process_compliance_requirements(compliance_status);

-- Audit indices
CREATE INDEX idx_process_audit_timestamp ON process_audit_log(change_timestamp);
CREATE INDEX idx_process_audit_process ON process_audit_log(process_id);

-- =====================================================
-- Views for Common Queries
-- =====================================================

-- Process Summary View
CREATE VIEW process_summary AS
SELECT 
    p.process_id,
    p.process_code,
    p.name,
    p.description,
    p.status,
    pc.name AS category_name,
    p.business_priority,
    p.risk_level,
    s.first_name || ' ' || s.last_name AS owner_name,
    s.email AS owner_email,
    o.name AS organization_name,
    p.frequency,
    p.current_success_rate,
    p.automation_level,
    p.updated_date,
    p.next_review_date
FROM processes p
LEFT JOIN process_categories pc ON p.category_id = pc.category_id
LEFT JOIN stakeholders s ON p.owner_stakeholder_id = s.stakeholder_id
LEFT JOIN organizations o ON p.organization_id = o.organization_id;

-- Process Dependencies View
CREATE VIEW process_dependencies AS
SELECT 
    pp.name AS parent_process,
    cp.name AS child_process,
    pr.relationship_type,
    pr.criticality,
    pr.dependency_type
FROM process_relationships pr
JOIN processes pp ON pr.parent_process_id = pp.process_id
JOIN processes cp ON pr.child_process_id = cp.process_id
WHERE pp.status = 'active' AND cp.status = 'active';

-- High Risk Processes View
CREATE VIEW high_risk_processes AS
SELECT 
    p.process_code,
    p.name,
    p.risk_level,
    COUNT(pr.risk_id) AS risk_count,
    AVG(pr.risk_score) AS average_risk_score,
    s.first_name || ' ' || s.last_name AS owner_name
FROM processes p
LEFT JOIN process_risks pr ON p.process_id = pr.process_id
LEFT JOIN stakeholders s ON p.owner_stakeholder_id = s.stakeholder_id
WHERE p.risk_level IN ('high', 'very-high') AND p.status = 'active'
GROUP BY p.process_id, p.process_code, p.name, p.risk_level, s.first_name, s.last_name
ORDER BY average_risk_score DESC;

-- Process Improvement Opportunities View
CREATE VIEW improvement_opportunities AS
SELECT 
    p.process_code,
    p.name AS process_name,
    pi.title,
    pi.improvement_type,
    pi.priority,
    pi.status,
    pi.expected_benefits,
    pi.annual_savings_estimate,
    s.first_name || ' ' || s.last_name AS owner_name
FROM process_improvements pi
JOIN processes p ON pi.process_id = p.process_id
LEFT JOIN stakeholders s ON pi.owner_stakeholder_id = s.stakeholder_id
WHERE pi.status IN ('identified', 'planned', 'in-progress')
ORDER BY pi.priority, pi.annual_savings_estimate DESC;

-- =====================================================
-- Comments and Documentation
-- =====================================================

COMMENT ON TABLE processes IS 'Main table storing all business process information';
COMMENT ON TABLE process_categories IS 'Hierarchical categorization of processes';
COMMENT ON TABLE systems IS 'IT systems and applications inventory';
COMMENT ON TABLE stakeholders IS 'Directory of people involved in processes';
COMMENT ON TABLE process_relationships IS 'Parent-child and dependency relationships between processes';
COMMENT ON TABLE process_performance_history IS 'Historical performance metrics for trend analysis';
COMMENT ON TABLE process_risks IS 'Risk assessment and mitigation for each process';
COMMENT ON TABLE process_improvements IS 'Identified opportunities for process enhancement';

-- =====================================================
-- Triggers for Audit Trail
-- =====================================================

-- Function to log changes
CREATE OR REPLACE FUNCTION log_process_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO process_audit_log (
            process_id, table_name, action, old_values, changed_by_stakeholder_id, change_timestamp
        ) VALUES (
            OLD.process_id, TG_TABLE_NAME, TG_OP, to_jsonb(OLD), 
            COALESCE(current_setting('app.current_user_id', true)::INTEGER, 0),
            CURRENT_TIMESTAMP
        );
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO process_audit_log (
            process_id, table_name, action, old_values, new_values,
            changed_by_stakeholder_id, change_timestamp
        ) VALUES (
            NEW.process_id, TG_TABLE_NAME, TG_OP, to_jsonb(OLD), to_jsonb(NEW),
            COALESCE(current_setting('app.current_user_id', true)::INTEGER, 0),
            CURRENT_TIMESTAMP
        );
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO process_audit_log (
            process_id, table_name, action, new_values,
            changed_by_stakeholder_id, change_timestamp
        ) VALUES (
            NEW.process_id, TG_TABLE_NAME, TG_OP, to_jsonb(NEW),
            COALESCE(current_setting('app.current_user_id', true)::INTEGER, 0),
            CURRENT_TIMESTAMP
        );
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Apply audit triggers to key tables
CREATE TRIGGER trigger_audit_processes
    AFTER INSERT OR UPDATE OR DELETE ON processes
    FOR EACH ROW EXECUTE FUNCTION log_process_changes();

CREATE TRIGGER trigger_audit_process_steps
    AFTER INSERT OR UPDATE OR DELETE ON process_steps
    FOR EACH ROW EXECUTE FUNCTION log_process_changes();

-- =====================================================
-- Functions for Data Quality and Validation
-- =====================================================

-- Function to calculate process quality score
CREATE OR REPLACE FUNCTION calculate_process_quality_score(p_process_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    quality_score INTEGER := 0;
    required_fields_count INTEGER := 0;
    filled_fields_count INTEGER := 0;
BEGIN
    -- Check required fields completion
    SELECT 
        CASE WHEN name IS NOT NULL AND name != '' THEN 1 ELSE 0 END +
        CASE WHEN description IS NOT NULL AND description != '' THEN 1 ELSE 0 END +
        CASE WHEN purpose IS NOT NULL AND purpose != '' THEN 1 ELSE 0 END +
        CASE WHEN owner_stakeholder_id IS NOT NULL THEN 1 ELSE 0 END +
        CASE WHEN category_id IS NOT NULL THEN 1 ELSE 0 END +
        CASE WHEN frequency IS NOT NULL THEN 1 ELSE 0 END +
        CASE WHEN business_priority IS NOT NULL THEN 1 ELSE 0 END
    INTO filled_fields_count
    FROM processes 
    WHERE process_id = p_process_id;
    
    required_fields_count := 7;
    quality_score := (filled_fields_count * 100) / required_fields_count;
    
    -- Bonus points for additional documentation
    IF EXISTS (SELECT 1 FROM process_steps WHERE process_id = p_process_id) THEN
        quality_score := quality_score + 5;
    END IF;
    
    IF EXISTS (SELECT 1 FROM process_risks WHERE process_id = p_process_id) THEN
        quality_score := quality_score + 5;
    END IF;
    
    IF EXISTS (SELECT 1 FROM process_kpis WHERE process_id = p_process_id) THEN
        quality_score := quality_score + 5;
    END IF;
    
    RETURN LEAST(quality_score, 100);
END;
$$ LANGUAGE plpgsql;