# Jira Task Breakdown Structure - Current State Architecture Assessment

## Project Configuration

**Project Key**: ARCH  
**Project Name**: Current State Architecture Assessment  
**Duration**: 8 Weeks  
**Methodology**: Iterative (Info Gathering → Draft → Feedback → Final Review → Final)

---

## Epic Structure

### Epic 1: Service Discovery & Inventory (Weeks 1-2)
**Epic Key**: ARCH-Epic-01  
**Summary**: Comprehensive discovery and cataloging of all services across 2 primary systems + infrastructure  
**Story Points**: 89  
**Priority**: Highest  

#### Week 1 Stories

**ARCH-001**: Conduct System 1 Stakeholder Interviews  
*Story Points: 8*  
*Priority: High*  
*Labels: discovery, stakeholder-engagement*
```
Acceptance Criteria:
- [ ] Interview 3-5 System 1 stakeholders (2 hours each)
- [ ] Document all services mentioned during interviews
- [ ] Identify service owners and contacts
- [ ] Record service dependencies mentioned
- [ ] Complete interview summary within 24 hours
- [ ] Stakeholder validation of summary within 48 hours
```

**ARCH-002**: Create System 1 Service Catalog  
*Story Points: 13*  
*Priority: High*  
*Labels: discovery, documentation*
```
Acceptance Criteria:
- [ ] Catalog minimum 10-15 services for System 1
- [ ] Include service name, purpose, owner, technology stack
- [ ] Document service boundaries and responsibilities
- [ ] Identify internal vs external services
- [ ] Create initial dependency map
- [ ] Service catalog approved by System 1 stakeholders
```

**ARCH-003**: Conduct System 2 Stakeholder Interviews  
*Story Points: 8*  
*Priority: High*  
*Labels: discovery, stakeholder-engagement*
```
Acceptance Criteria:
- [ ] Interview 3-5 System 2 stakeholders (2 hours each)
- [ ] Document all services mentioned during interviews
- [ ] Identify service owners and contacts
- [ ] Record service dependencies mentioned
- [ ] Complete interview summary within 24 hours
- [ ] Stakeholder validation of summary within 48 hours
```

**ARCH-004**: Create System 2 Service Catalog  
*Story Points: 13*  
*Priority: High*  
*Labels: discovery, documentation*
```
Acceptance Criteria:
- [ ] Catalog minimum 10-15 services for System 2
- [ ] Include service name, purpose, owner, technology stack
- [ ] Document service boundaries and responsibilities
- [ ] Identify internal vs external services
- [ ] Create initial dependency map
- [ ] Service catalog approved by System 2 stakeholders
```

**ARCH-005**: Identify Cross-System Dependencies  
*Story Points: 8*  
*Priority: High*  
*Labels: discovery, integration*
```
Acceptance Criteria:
- [ ] Map all interactions between System 1 and System 2
- [ ] Document communication protocols used
- [ ] Identify shared databases or storage
- [ ] Record integration patterns
- [ ] Create cross-system dependency matrix
- [ ] Validate dependencies with both system teams
```

**ARCH-006**: Draft Service Inventory v1.0  
*Story Points: 5*  
*Priority: High*  
*Labels: documentation, milestone*
```
Acceptance Criteria:
- [ ] Consolidate System 1 and System 2 catalogs
- [ ] Create unified service naming convention
- [ ] Generate preliminary service inventory
- [ ] Include all discovered dependencies
- [ ] Present to stakeholder feedback session
- [ ] Document feedback and required changes
```

#### Week 2 Stories

**ARCH-007**: Map Infrastructure Services  
*Story Points: 13*  
*Priority: High*  
*Labels: discovery, infrastructure*
```
Acceptance Criteria:
- [ ] Identify all infrastructure components supporting both systems
- [ ] Document compute, network, storage services
- [ ] Map infrastructure service dependencies
- [ ] Include cloud and on-premise components
- [ ] Document infrastructure ownership
- [ ] Infrastructure team validation of mapping
```

**ARCH-008**: Document Database Dependencies  
*Story Points: 8*  
*Priority: High*  
*Labels: discovery, data*
```
Acceptance Criteria:
- [ ] Catalog all databases used by both systems
- [ ] Document database types and versions
- [ ] Map application-to-database relationships
- [ ] Identify shared vs dedicated databases
- [ ] Document data flow patterns
- [ ] Database team validation of documentation
```

**ARCH-009**: Identify Network Services  
*Story Points: 5*  
*Priority: Medium*  
*Labels: discovery, network*
```
Acceptance Criteria:
- [ ] Map network topology for both systems
- [ ] Document load balancers, proxies, CDNs
- [ ] Identify network security components
- [ ] Document network dependencies
- [ ] Include external network services
- [ ] Network team validation of mapping
```

**ARCH-010**: Create Service Dependency Matrix  
*Story Points: 13*  
*Priority: High*  
*Labels: documentation, analysis*
```
Acceptance Criteria:
- [ ] Create comprehensive dependency matrix
- [ ] Include all service-to-service relationships
- [ ] Document dependency types (sync/async, critical/optional)
- [ ] Identify circular dependencies
- [ ] Create visual dependency map
- [ ] Architecture team review and approval
```

**ARCH-011**: Draft Complete Service Inventory v2.0  
*Story Points: 8*  
*Priority: High*  
*Labels: documentation, milestone*
```
Acceptance Criteria:
- [ ] Integrate infrastructure and application services
- [ ] Include comprehensive dependency information
- [ ] Add service categorization (core, supporting, external)
- [ ] Document service health monitoring status
- [ ] Create service inventory dashboard
- [ ] Stakeholder review session completion
```

**ARCH-012**: Infrastructure Feedback Session  
*Story Points: 3*  
*Priority: Medium*  
*Labels: validation, stakeholder-engagement*
```
Acceptance Criteria:
- [ ] Present infrastructure mapping to infrastructure team
- [ ] Collect feedback on accuracy and completeness
- [ ] Document any missing infrastructure components
- [ ] Validate infrastructure dependency relationships
- [ ] Update inventory based on feedback
- [ ] Obtain infrastructure team sign-off
```

### Epic 2: C4 Context Modeling (Weeks 3-4)
**Epic Key**: ARCH-Epic-02  
**Summary**: Create C4 Context diagrams for both primary systems showing external relationships  
**Story Points**: 71  
**Priority**: High  

#### Week 3 Stories

**ARCH-013**: Identify System 1 Users and Actors  
*Story Points: 5*  
*Priority: High*  
*Labels: modeling, analysis*
```
Acceptance Criteria:
- [ ] Identify all user types interacting with System 1
- [ ] Document user roles and permissions
- [ ] Include both human users and other systems
- [ ] Document user interaction patterns
- [ ] Validate with System 1 stakeholders
- [ ] Create user/actor registry
```

**ARCH-014**: Create System 1 C4 Context Diagram  
*Story Points: 13*  
*Priority: High*  
*Labels: modeling, documentation*
```
Acceptance Criteria:
- [ ] Follow C4 notation standards
- [ ] Show System 1 as central system
- [ ] Include all identified users/actors
- [ ] Show all external systems interactions
- [ ] Document relationship purposes
- [ ] Stakeholder validation >85% approval
```

**ARCH-015**: Identify System 2 Users and Actors  
*Story Points: 5*  
*Priority: High*  
*Labels: modeling, analysis*
```
Acceptance Criteria:
- [ ] Identify all user types interacting with System 2
- [ ] Document user roles and permissions
- [ ] Include both human users and other systems
- [ ] Document user interaction patterns
- [ ] Validate with System 2 stakeholders
- [ ] Create user/actor registry
```

**ARCH-016**: Create System 2 C4 Context Diagram  
*Story Points: 13*  
*Priority: High*  
*Labels: modeling, documentation*
```
Acceptance Criteria:
- [ ] Follow C4 notation standards
- [ ] Show System 2 as central system
- [ ] Include all identified users/actors
- [ ] Show all external systems interactions
- [ ] Document relationship purposes
- [ ] Stakeholder validation >85% approval
```

**ARCH-017**: Document Cross-System Contexts  
*Story Points: 8*  
*Priority: High*  
*Labels: modeling, integration*
```
Acceptance Criteria:
- [ ] Document how System 1 and System 2 contexts overlap
- [ ] Identify shared external systems
- [ ] Document shared user/actor types
- [ ] Create combined context view
- [ ] Validate cross-system relationships
- [ ] Architecture team review and approval
```

**ARCH-018**: Context Diagram Feedback Session  
*Story Points: 3*  
*Priority: Medium*  
*Labels: validation, stakeholder-engagement*
```
Acceptance Criteria:
- [ ] Present both context diagrams to stakeholders
- [ ] Collect feedback on accuracy and completeness
- [ ] Document required changes
- [ ] Validate external system relationships
- [ ] Update diagrams based on feedback
- [ ] Obtain stakeholder approval for contexts
```

#### Week 4 Stories

**ARCH-019**: Refine System 1 Context Boundaries  
*Story Points: 5*  
*Priority: High*  
*Labels: modeling, refinement*
```
Acceptance Criteria:
- [ ] Incorporate stakeholder feedback
- [ ] Refine system boundary definitions
- [ ] Update external system relationships
- [ ] Improve diagram clarity and accuracy
- [ ] Document boundary rationale
- [ ] System 1 stakeholder final approval
```

**ARCH-020**: Refine System 2 Context Boundaries  
*Story Points: 5*  
*Priority: High*  
*Labels: modeling, refinement*
```
Acceptance Criteria:
- [ ] Incorporate stakeholder feedback
- [ ] Refine system boundary definitions
- [ ] Update external system relationships
- [ ] Improve diagram clarity and accuracy
- [ ] Document boundary rationale
- [ ] System 2 stakeholder final approval
```

**ARCH-021**: Create Integrated Context View  
*Story Points: 8*  
*Priority: High*  
*Labels: modeling, integration*
```
Acceptance Criteria:
- [ ] Combine both system contexts into single view
- [ ] Show relationships between the two systems
- [ ] Include all external systems
- [ ] Resolve overlapping contexts
- [ ] Create comprehensive context landscape
- [ ] Architecture team validation
```

**ARCH-022**: Validate External Dependencies  
*Story Points: 5*  
*Priority: High*  
*Labels: validation, analysis*
```
Acceptance Criteria:
- [ ] Confirm all external system relationships
- [ ] Validate dependency criticality
- [ ] Document dependency SLAs where available
- [ ] Identify potential single points of failure
- [ ] Create external dependency risk assessment
- [ ] External system owner confirmations
```

**ARCH-023**: Final Context Diagram Review  
*Story Points: 3*  
*Priority: High*  
*Labels: validation, milestone*
```
Acceptance Criteria:
- [ ] Present final context diagrams
- [ ] Obtain final stakeholder sign-off
- [ ] Document any remaining issues
- [ ] Confirm diagram storage location
- [ ] Update diagram metadata
- [ ] Complete context modeling phase
```

**ARCH-024**: Context Phase Sign-Off  
*Story Points: 2*  
*Priority: High*  
*Labels: milestone, governance*
```
Acceptance Criteria:
- [ ] Architecture team formal review
- [ ] All stakeholder approvals documented
- [ ] Context diagrams stored in repository
- [ ] Phase completion metrics calculated
- [ ] Lessons learned documented
- [ ] Container phase readiness confirmed
```

### Epic 3: C4 Container Modeling (Weeks 5-6)
**Epic Key**: ARCH-Epic-03  
**Summary**: Create detailed C4 Container diagrams showing internal service structure  
**Story Points**: 73  
**Priority**: High  

#### Week 5 Stories

**ARCH-025**: Decompose System 1 Containers  
*Story Points: 13*  
*Priority: High*  
*Labels: modeling, analysis*
```
Acceptance Criteria:
- [ ] Identify all applications within System 1
- [ ] Identify all databases within System 1
- [ ] Document container responsibilities
- [ ] Map container technologies
- [ ] Document container communication patterns
- [ ] System 1 technical team validation
```

**ARCH-026**: Create System 1 C4 Container Diagram  
*Story Points: 13*  
*Priority: High*  
*Labels: modeling, documentation*
```
Acceptance Criteria:
- [ ] Follow C4 container notation standards
- [ ] Show all identified containers
- [ ] Include technology choices for each container
- [ ] Document container relationships
- [ ] Show data flow between containers
- [ ] Technical stakeholder approval >85%
```

**ARCH-027**: Decompose System 2 Containers  
*Story Points: 13*  
*Priority: High*  
*Labels: modeling, analysis*
```
Acceptance Criteria:
- [ ] Identify all applications within System 2
- [ ] Identify all databases within System 2
- [ ] Document container responsibilities
- [ ] Map container technologies
- [ ] Document container communication patterns
- [ ] System 2 technical team validation
```

**ARCH-028**: Create System 2 C4 Container Diagram  
*Story Points: 13*  
*Priority: High*  
*Labels: modeling, documentation*
```
Acceptance Criteria:
- [ ] Follow C4 container notation standards
- [ ] Show all identified containers
- [ ] Include technology choices for each container
- [ ] Document container relationships
- [ ] Show data flow between containers
- [ ] Technical stakeholder approval >85%
```

**ARCH-029**: Map Inter-Container Communications  
*Story Points: 8*  
*Priority: High*  
*Labels: modeling, integration*
```
Acceptance Criteria:
- [ ] Document all container-to-container communications
- [ ] Include communication protocols (HTTP, messaging, etc.)
- [ ] Map synchronous vs asynchronous communications
- [ ] Document communication security measures
- [ ] Create communication flow diagrams
- [ ] Technical team validation
```

**ARCH-030**: Container Diagram Feedback Session  
*Story Points: 3*  
*Priority: Medium*  
*Labels: validation, stakeholder-engagement*
```
Acceptance Criteria:
- [ ] Present container diagrams to technical teams
- [ ] Collect detailed technical feedback
- [ ] Document accuracy concerns
- [ ] Validate container boundaries
- [ ] Update diagrams based on feedback
- [ ] Technical stakeholder approval
```

#### Week 6 Stories

**ARCH-031**: Map Cross-System Container Interactions  
*Story Points: 8*  
*Priority: High*  
*Labels: modeling, integration*
```
Acceptance Criteria:
- [ ] Identify containers that communicate across systems
- [ ] Document cross-system communication protocols
- [ ] Map data sharing between systems
- [ ] Document integration patterns
- [ ] Create cross-system container mapping
- [ ] Both technical teams validation
```

**ARCH-032**: Create Integrated Container View  
*Story Points: 13*  
*Priority: High*  
*Labels: modeling, integration*
```
Acceptance Criteria:
- [ ] Combine both system container diagrams
- [ ] Show cross-system container relationships
- [ ] Include shared infrastructure containers
- [ ] Resolve container overlaps
- [ ] Create comprehensive container landscape
- [ ] Architecture team approval
```

**ARCH-033**: Map Containers to Infrastructure  
*Story Points: 8*  
*Priority: High*  
*Labels: modeling, infrastructure*
```
Acceptance Criteria:
- [ ] Map each container to deployment infrastructure
- [ ] Document container hosting details
- [ ] Include scaling and availability information
- [ ] Map container dependencies on infrastructure
- [ ] Document container resource requirements
- [ ] Infrastructure team validation
```

**ARCH-034**: Document Deployment Environments  
*Story Points: 5*  
*Priority: High*  
*Labels: documentation, deployment*
```
Acceptance Criteria:
- [ ] Document all deployment environments (dev/test/prod)
- [ ] Map container deployment variations by environment
- [ ] Document environment-specific configurations
- [ ] Include environment promotion process
- [ ] Document environment dependencies
- [ ] Operations team validation
```

**ARCH-035**: Final Container Diagram Review  
*Story Points: 3*  
*Priority: High*  
*Labels: validation, milestone*
```
Acceptance Criteria:
- [ ] Present final container diagrams
- [ ] Obtain technical stakeholder sign-off
- [ ] Document any outstanding issues
- [ ] Confirm container-to-deployment mapping
- [ ] Update container diagram metadata
- [ ] Complete container modeling phase
```

**ARCH-036**: Container Phase Sign-Off  
*Story Points: 2*  
*Priority: High*  
*Labels: milestone, governance*
```
Acceptance Criteria:
- [ ] Architecture team formal review
- [ ] All technical approvals documented
- [ ] Container diagrams stored in repository
- [ ] Phase completion metrics calculated
- [ ] Lessons learned documented
- [ ] Deployment phase readiness confirmed
```

### Epic 4: Deployment Diagrams & Finalization (Weeks 7-8)
**Epic Key**: ARCH-Epic-04  
**Summary**: Create deployment diagrams and complete the Context→Container→Deployment flow  
**Story Points**: 62  
**Priority**: High  

#### Week 7 Stories

**ARCH-037**: Create System 1 Deployment Diagram  
*Story Points: 13*  
*Priority: High*  
*Labels: modeling, deployment*
```
Acceptance Criteria:
- [ ] Follow C4 deployment notation standards
- [ ] Show all deployment nodes for System 1
- [ ] Map containers to deployment nodes
- [ ] Include infrastructure components
- [ ] Document deployment relationships
- [ ] Infrastructure team approval >85%
```

**ARCH-038**: Create System 2 Deployment Diagram  
*Story Points: 13*  
*Priority: High*  
*Labels: modeling, deployment*
```
Acceptance Criteria:
- [ ] Follow C4 deployment notation standards
- [ ] Show all deployment nodes for System 2
- [ ] Map containers to deployment nodes
- [ ] Include infrastructure components
- [ ] Document deployment relationships
- [ ] Infrastructure team approval >85%
```

**ARCH-039**: Create Integrated Deployment View  
*Story Points: 13*  
*Priority: High*  
*Labels: modeling, integration*
```
Acceptance Criteria:
- [ ] Combine both system deployment diagrams
- [ ] Show shared infrastructure components
- [ ] Include network connections
- [ ] Document deployment dependencies
- [ ] Create complete deployment landscape
- [ ] Operations team validation
```

**ARCH-040**: Map Deployment Dependencies  
*Story Points: 8*  
*Priority: High*  
*Labels: analysis, deployment*
```
Acceptance Criteria:
- [ ] Identify all deployment-level dependencies
- [ ] Document infrastructure dependencies
- [ ] Map network dependencies
- [ ] Include external service dependencies
- [ ] Create deployment dependency matrix
- [ ] Risk assessment for critical dependencies
```

**ARCH-041**: Validate Context→Container→Deployment Flow  
*Story Points: 8*  
*Priority: High*  
*Labels: validation, integration*
```
Acceptance Criteria:
- [ ] Ensure consistency across all three diagram levels
- [ ] Validate traceability from context to deployment
- [ ] Check for gaps in the flow
- [ ] Document flow relationships
- [ ] Create diagram traceability matrix
- [ ] Architecture team validation
```

**ARCH-042**: Deployment Diagram Feedback Session  
*Story Points: 3*  
*Priority: Medium*  
*Labels: validation, stakeholder-engagement*
```
Acceptance Criteria:
- [ ] Present deployment diagrams to operations team
- [ ] Collect infrastructure feedback
- [ ] Document deployment accuracy concerns
- [ ] Validate deployment relationships
- [ ] Update diagrams based on feedback
- [ ] Operations team approval
```

#### Week 8 Stories

**ARCH-043**: Finalize All C4 Diagrams  
*Story Points: 8*  
*Priority: High*  
*Labels: finalization, documentation*
```
Acceptance Criteria:
- [ ] Apply consistent styling across all diagrams
- [ ] Ensure all diagrams follow C4 standards
- [ ] Update diagram metadata and versioning
- [ ] Create diagram legend and notation guide
- [ ] Store all diagrams in agreed repository
- [ ] Quality assurance review completion
```

**ARCH-044**: Complete Service Inventory  
*Story Points: 5*  
*Priority: High*  
*Labels: finalization, documentation*
```
Acceptance Criteria:
- [ ] Finalize service inventory with all discoveries
- [ ] Include complete service metadata
- [ ] Map services to diagram elements
- [ ] Create service inventory dashboard
- [ ] Document service inventory maintenance process
- [ ] Service owner validation of final inventory
```

**ARCH-045**: Create Diagram Traceability Matrix  
*Story Points: 5*  
*Priority: High*  
*Labels: documentation, traceability*
```
Acceptance Criteria:
- [ ] Map elements across context, container, deployment
- [ ] Create service-to-diagram mapping
- [ ] Document diagram relationships
- [ ] Include change impact analysis
- [ ] Create traceability dashboard
- [ ] Architecture team approval
```

**ARCH-046**: Final Stakeholder Validation  
*Story Points: 5*  
*Priority: High*  
*Labels: validation, milestone*
```
Acceptance Criteria:
- [ ] Present complete architecture to all stakeholders
- [ ] Collect final validation from all stakeholder groups
- [ ] Document any remaining issues
- [ ] Obtain final sign-offs
- [ ] Create stakeholder approval matrix
- [ ] Address any critical feedback
```

**ARCH-047**: Final Architecture Presentation  
*Story Points: 8*  
*Priority: High*  
*Labels: presentation, milestone*
```
Acceptance Criteria:
- [ ] Prepare executive presentation
- [ ] Include architecture overview and key findings
- [ ] Present Context→Container→Deployment flow
- [ ] Demonstrate service inventory value
- [ ] Document presentation feedback
- [ ] Executive stakeholder approval
```

**ARCH-048**: Project Closure Documentation  
*Story Points: 3*  
*Priority: Medium*  
*Labels: closure, documentation*
```
Acceptance Criteria:
- [ ] Create project completion report
- [ ] Document lessons learned
- [ ] Archive all project artifacts
- [ ] Create handover documentation
- [ ] Document maintenance procedures
- [ ] Complete project metrics calculation
```

### Epic 5: Project Management & Coordination (Weeks 1-8)
**Epic Key**: ARCH-Epic-05  
**Summary**: Ongoing project management, coordination, and quality assurance activities  
**Story Points**: 45  
**Priority**: Medium  

**ARCH-049**: Weekly Project Coordination (8 weeks)  
*Story Points: 21*  
*Priority: Medium*  
*Labels: coordination, management*
```
Acceptance Criteria:
- [ ] Weekly team standup meetings (8 weeks)
- [ ] Weekly stakeholder status reports
- [ ] Risk and issue tracking
- [ ] Resource coordination
- [ ] Schedule management
- [ ] Budget tracking
```

**ARCH-050**: Quality Assurance Reviews (4 phases)  
*Story Points: 13*  
*Priority: Medium*  
*Labels: quality, validation*
```
Acceptance Criteria:
- [ ] Service inventory QA review (Week 2)
- [ ] Context diagram QA review (Week 4)
- [ ] Container diagram QA review (Week 6)
- [ ] Final deliverables QA review (Week 8)
```

**ARCH-051**: Stakeholder Communication Management  
*Story Points: 8*  
*Priority: Medium*  
*Labels: communication, stakeholder-engagement*
```
Acceptance Criteria:
- [ ] Manage stakeholder calendar coordination
- [ ] Distribute regular communications
- [ ] Manage feedback collection and response
- [ ] Escalate issues as needed
- [ ] Maintain stakeholder satisfaction >85%
```

**ARCH-052**: Jira Project Management  
*Story Points: 3*  
*Priority: Low*  
*Labels: tools, management*
```
Acceptance Criteria:
- [ ] Maintain Jira project structure
- [ ] Update task progress regularly
- [ ] Generate progress reports
- [ ] Manage sprint planning (if using sprints)
- [ ] Track project metrics
```

---

## Implementation Guidelines

### Sprint Structure (Optional)
If using Scrum methodology:
- **2-week sprints** aligning with project phases
- **Sprint 1**: Service Discovery System 1 (ARCH-001 to ARCH-006)
- **Sprint 2**: Service Discovery System 2 + Infrastructure (ARCH-007 to ARCH-012)
- **Sprint 3**: Context Modeling (ARCH-013 to ARCH-018)
- **Sprint 4**: Context Refinement (ARCH-019 to ARCH-024)
- **Sprint 5**: Container Modeling (ARCH-025 to ARCH-030)
- **Sprint 6**: Container Integration (ARCH-031 to ARCH-036)
- **Sprint 7**: Deployment Modeling (ARCH-037 to ARCH-042)
- **Sprint 8**: Finalization (ARCH-043 to ARCH-048)

### Task Assignment Guidelines
- **Lead Architect**: Complex modeling tasks (13+ story points)
- **Business Analyst**: Discovery and documentation tasks (5-8 points)
- **Technical Lead**: Integration and validation tasks (8-13 points)
- **Project Manager**: Coordination tasks (2-5 points)

### Definition of Done
- [ ] Acceptance criteria 100% complete
- [ ] Peer review completed
- [ ] Stakeholder validation obtained (where required)
- [ ] Documentation updated
- [ ] Quality standards met
- [ ] Jira task status updated

### Reporting Structure
- **Daily**: Individual task progress updates
- **Weekly**: Sprint/phase progress reports
- **Milestone**: Phase completion reports
- **Final**: Project completion report

---

*This Jira structure provides complete traceability, stakeholder management capabilities, and supports the iterative methodology while focusing exclusively on current state assessment.*