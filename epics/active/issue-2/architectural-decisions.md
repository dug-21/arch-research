# Architectural Decision Records (ADRs)

## ADR-001: Adoption of Model Context Protocol (MCP) for AI Coordination

### Status
Accepted

### Context
The system needs a standardized way to coordinate between Claude Code (the AI assistant) and the swarm orchestration system. Multiple options exist including custom protocols, REST APIs, or existing standards.

### Decision
We will use the Model Context Protocol (MCP) for all AI coordination tasks.

### Consequences
**Positive:**
- Standardized protocol ensures compatibility
- Supports both stdio and HTTP transports
- Well-defined tool registration and invocation patterns
- Future-proof as MCP gains adoption

**Negative:**
- Requires MCP server implementation
- Additional abstraction layer
- Limited to MCP-supported features

**Risks:**
- MCP specification changes might require updates
- Performance overhead of protocol translation

---

## ADR-002: SQLite for Persistent Memory Storage

### Status
Accepted

### Context
The swarm coordination system requires persistent storage for memory, state, and metrics. Options included file-based JSON, PostgreSQL, SQLite, or in-memory databases.

### Decision
Use SQLite as the primary storage mechanism for all persistent data.

### Consequences
**Positive:**
- Zero configuration database
- ACID compliance ensures data integrity
- Embedded database requires no separate process
- Excellent performance for local operations
- Easy backup and portability

**Negative:**
- Single-writer limitation
- Not suitable for distributed systems
- Limited concurrent access

**Risks:**
- Database corruption (mitigated by WAL mode)
- Size limitations (theoretical 281TB limit is not a concern)

---

## ADR-003: Mandatory Parallel Execution Pattern

### Status
Accepted

### Context
Swarm operations can be executed sequentially or in parallel. Performance testing showed significant improvements with parallel execution.

### Decision
All swarm operations MUST be executed in parallel using batch operations. Sequential execution is explicitly forbidden.

### Consequences
**Positive:**
- 2.8-4.4x performance improvement
- 32.3% token reduction
- Better resource utilization
- Improved user experience

**Negative:**
- More complex error handling
- Requires careful coordination design
- Higher memory usage during execution

**Risks:**
- Race conditions (mitigated by memory-based coordination)
- Resource exhaustion (mitigated by agent limits)

---

## ADR-004: Markdown-Based Documentation System

### Status
Accepted

### Context
Documentation needs to be version-controlled, human-readable, and tool-processable. Options included Word documents, wikis, databases, or Markdown.

### Decision
All documentation will be written in Markdown format with YAML frontmatter for metadata.

### Consequences
**Positive:**
- Git-friendly for version control
- Human-readable without special tools
- Wide ecosystem support
- Easy to generate and transform
- Supports diagrams via Mermaid

**Negative:**
- Limited formatting compared to rich documents
- Table handling can be cumbersome
- No built-in versioning within files

---

## ADR-005: Hook-Based Extension Architecture

### Status
Accepted

### Context
The system needs to be extensible without modifying core code. Options included plugins, configuration files, or event hooks.

### Decision
Implement a comprehensive hook system for all major operations (pre/post task, edit, command, etc.).

### Consequences
**Positive:**
- Clean extension points
- No core code modification needed
- Event-driven architecture
- Easy to disable/enable features

**Negative:**
- Performance overhead for hook execution
- Complexity in hook ordering
- Potential for hook conflicts

---

## ADR-006: Hybrid Methodology Support

### Status
Accepted

### Context
Users need flexibility in choosing development methodologies. Should the system enforce one methodology or support multiple?

### Decision
Support both traditional phase-gate and modern agile/prototyping methodologies with templates for each.

### Consequences
**Positive:**
- Flexibility for different project types
- Comprehensive methodology coverage
- User choice in approach
- Educational value

**Negative:**
- Increased complexity in templates
- More documentation to maintain
- Potential for methodology confusion

---

## ADR-007: Local-First Architecture

### Status
Accepted

### Context
The system could be cloud-based, hybrid, or entirely local. Privacy, performance, and availability were key concerns.

### Decision
Implement a local-first architecture with all processing and storage on the developer's machine.

### Consequences
**Positive:**
- Complete privacy and data control
- No internet dependency for core features
- Zero latency for operations
- No hosting costs

**Negative:**
- No built-in collaboration features
- Manual backup responsibility
- Limited to local machine resources

---

## ADR-008: Agent-Based Cognitive Patterns

### Status
Accepted

### Context
Task distribution could be random, round-robin, or based on specialized agents with different cognitive patterns.

### Decision
Implement specialized agents (researcher, coder, analyst, etc.) that represent different cognitive approaches to problems.

### Consequences
**Positive:**
- Better task-to-agent matching
- Specialized optimization per agent type
- More intuitive mental model
- Improved solution quality

**Negative:**
- Complexity in agent design
- Potential for agent imbalance
- Training requirements per agent type

---

## ADR-009: Memory-Based Inter-Agent Communication

### Status
Accepted

### Context
Agents need to communicate. Options included direct messaging, shared files, or shared memory.

### Decision
All inter-agent communication happens through the persistent memory store using namespace-based keys.

### Consequences
**Positive:**
- Persistent communication history
- No additional communication infrastructure
- Natural audit trail
- Supports async communication

**Negative:**
- Potential memory bottleneck
- Requires memory polling
- No real-time messaging

---

## ADR-010: CLI-First User Interface

### Status
Accepted

### Context
User interface options included web UI, desktop app, IDE plugin, or CLI.

### Decision
Implement a CLI-first interface with potential for future UI additions.

### Consequences
**Positive:**
- Fast development cycle
- Scriptable and automatable
- No UI framework dependencies
- Works in all environments

**Negative:**
- Steeper learning curve
- Limited visual feedback
- Text-only interaction

---

## ADR-011: Session-Based State Management

### Status
Accepted

### Context
State could be managed globally, per-project, or per-session.

### Decision
Implement session-based state management with automatic save/restore capabilities.

### Consequences
**Positive:**
- Clean separation between sessions
- Easy to resume work
- Natural checkpoint boundaries
- Supports experimentation

**Negative:**
- Session management overhead
- Potential for session proliferation
- Manual session selection

---

## ADR-012: Template-Driven Workflow Definition

### Status
Accepted

### Context
Workflows could be hardcoded, configured via UI, or template-based.

### Decision
Use template files (Markdown with YAML) to define all workflows and methodologies.

### Consequences
**Positive:**
- Version control friendly
- Easy to share and modify
- Self-documenting
- No compilation needed

**Negative:**
- Template syntax learning curve
- Limited runtime flexibility
- Potential for template errors

---

## Future Architectural Decisions

### Pending Decisions

1. **Cloud Synchronization**
   - Context: Users want to sync state across machines
   - Options: Cloud storage, P2P sync, Git-based sync
   - Status: Under consideration

2. **Plugin Architecture**
   - Context: Third-party extensions beyond hooks
   - Options: npm packages, dynamic loading, sandboxed execution
   - Status: Research phase

3. **Multi-Language Support**
   - Context: Support beyond Node.js ecosystem
   - Options: Language servers, FFI, microservices
   - Status: Future consideration

4. **Distributed Swarm Execution**
   - Context: Scale beyond single machine
   - Options: Container orchestration, cloud functions, grid computing
   - Status: Long-term vision

### Decision-Making Process

1. **Proposal**: Problem statement and options
2. **Research**: Investigate each option
3. **Prototype**: Test promising approaches
4. **Review**: Team and community feedback
5. **Decision**: Document in ADR format
6. **Implementation**: Execute decision
7. **Retrospective**: Review after implementation

This ADR document will be updated as new architectural decisions are made.