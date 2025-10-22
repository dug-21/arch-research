# 5-Phase Creation Workflow - Detailed Implementation

This document provides comprehensive details for each phase of the development workflow template.

---

## PHASE 1: Wild Idea + Deep Research

**Duration**: Variable (1-4 hours)
**Participants**: User + Scout Explorer agents + Researcher agents
**Tools**: Goalie GOAP search, Web research, AgentDB vector search

### Workflow

```bash
# Launch Phase 1
.agentic/scripts/phase-1-research.sh "<wild idea description>"
```

### What Happens

1. **User Provides Wild Idea**
   - Rough concept or problem statement
   - No formal structure required
   - Example: "What if we could automatically generate API documentation from code comments using AI?"

2. **Scout Explorer Agents Launch**
   ```javascript
   mcp__goalie__goap_search({
     query: "AI-powered API documentation generation from code comments",
     mode: "web",
     enableReasoning: true
   })
   ```

3. **Research Activities**
   - **Prior Art Analysis**: Search for existing solutions
   - **Feasibility Validation**: Technical constraints, dependencies
   - **Similar Projects**: Vector search AgentDB for related work
   - **Web Research**: Latest approaches, libraries, frameworks

4. **Output**
   - Research report in `.agentic/research/phase-1-report.md`
   - Feasibility score (0-1.0)
   - Recommended next steps
   - Key insights and constraints

---

## PHASE 2: Formalize Scope/Value + High-Level Architecture

**Duration**: 1-3 hours
**Participants**: User + Collective Intelligence + System Architect agents
**Tools**: AgentDB, Spec templates, Architecture diagram tools

### Workflow

```bash
# Launch Phase 2 (iterative)
.agentic/scripts/phase-2-formalize.sh
```

### What Happens

1. **Scope Definition (Iterative)**
   - User discusses findings from Phase 1 with AI agents
   - Agents ask clarifying questions about scope
   - Iterate until full scope is defined

2. **Value Proposition Analysis**
   - **Collective Intelligence Agent** analyzes:
     - Target users
     - Key benefits
     - Competitive advantages
     - Success metrics

3. **High-Level Architecture Definition**
   - **System Architect Agent** proposes:
     - Major components
     - Integration points
     - Technology stack recommendations
     - Data flow (high-level)

4. **Output**
   - Scope document: `.agentic/specs/scope-v1.md`
   - Value proposition: `.agentic/specs/value-prop.md`
   - High-level architecture: `.agentic/architecture/overview.md`
   - Component list: `.agentic/architecture/components.yml`

---

## PHASE 3: SPARC Planning (Formal)

**Duration**: 2-4 hours
**Participants**: SPARC specialist agents (Spec, Pseudocode, Architect)
**Tools**: SPARC methodology, AgentDB pattern search

### Workflow

```bash
# Launch SPARC Planning
.agentic/scripts/phase-3-sparc.sh
```

### Sub-Phases

#### 3.1 Specification

**SPARC Specification Agent**:
- Transforms scope/value into formal requirements
- Defines acceptance criteria
- Documents constraints and edge cases
- Creates test scenarios

**Output**: `.agentic/specs/formal-spec.md`

```markdown
# Formal Specification: AI-Powered API Docs

## Functional Requirements
FR-1: System shall analyze code comments in supported languages (JS, TS, Python, Go)
FR-2: System shall generate OpenAPI 3.0 specifications from analyzed comments
FR-3: System shall provide real-time preview of generated documentation
...

## Non-Functional Requirements
NFR-1: Code analysis shall complete within 5 seconds for files up to 10K lines
NFR-2: System shall support concurrent analysis of up to 100 files
...

## Acceptance Criteria
AC-1: Given a JavaScript file with JSDoc comments, system generates valid OpenAPI spec
AC-2: Generated spec includes all HTTP methods, parameters, and response schemas
...

## Edge Cases
EC-1: Handle files with mixed comment styles (JSDoc + inline)
EC-2: Handle missing or incomplete comment blocks
...
```

#### 3.2 Pseudocode

**SPARC Pseudocode Agent**:
- Designs algorithm logic flow
- Breaks down complex operations
- Identifies reusable patterns (via AgentDB vector search)

**Output**: `.agentic/pseudocode/algorithms.md`

```
FUNCTION analyzeCodeFile(filePath, language):
  1. READ file contents
  2. PARSE syntax tree (language-specific parser)
  3. EXTRACT comment blocks:
     a. Identify comment syntax by language
     b. Parse JSDoc/Sphinx/GoDoc tags
     c. Map to OpenAPI components
  4. GENERATE OpenAPI schema:
     a. For each function:
        - Extract HTTP method (from @method tag)
        - Extract route path (from @route tag)
        - Build parameter schema (from @param tags)
        - Build response schema (from @returns tag)
  5. VALIDATE generated schema
  6. RETURN OpenAPI object

FUNCTION generateDocumentation(openapiSpec):
  1. VALIDATE spec against OpenAPI 3.0 schema
  2. RENDER documentation (Swagger UI / Redoc)
  3. RETURN rendered HTML
```

#### 3.3 Architecture

**SPARC Architecture Agent**:
- Technical component design
- API specifications
- Database schema (if needed)
- Integration architecture
- Deployment architecture

**Output**: `.agentic/architecture/technical-design.md`

```markdown
# Technical Architecture: AI-Powered API Docs

## Component Diagram
```
┌─────────────────────────────────────────┐
│  CLI / VS Code Extension                │
│  (User Interface)                       │
└───────────┬─────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│  Code Analyzer Service                  │
│  • File watcher                         │
│  • Language-specific parsers            │
│  • Comment extractor                    │
└───────────┬─────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│  OpenAPI Generator                      │
│  • Schema builder                       │
│  • Validator (OpenAPI 3.0)              │
└───────────┬─────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│  Documentation Renderer                 │
│  • Swagger UI integration               │
│  • Real-time preview                    │
└─────────────────────────────────────────┘
```

## Technology Stack
- **Parser**: tree-sitter (multi-language AST parsing)
- **OpenAPI**: @apidevtools/swagger-parser (validation)
- **Rendering**: swagger-ui-react
- **Storage**: AgentDB (pattern caching, optional)
- **Testing**: Jest + Supertest

## API Endpoints (if building as service)
- POST /api/analyze - Analyze code file
- GET /api/spec/:id - Retrieve generated spec
- GET /api/preview/:id - Preview documentation
```

### Final SPARC Output

**Comprehensive package**: `.agentic/sparc/complete-spec-v1.0/`
- `specification.md` - Formal requirements
- `pseudocode.md` - Algorithm designs
- `architecture.md` - Technical design
- `test-plan.md` - Testing strategy
- `acceptance-criteria.json` - Machine-readable criteria

---

## PHASE 4: Human Approval Checkpoint

**Duration**: 15-60 minutes
**Participants**: User only (review mode)
**Tools**: Diff viewer, SPARC spec viewer

### Workflow

```bash
# Launch approval workflow (interactive)
.agentic/scripts/phase-4-approve.sh
```

### What Happens

1. **SPARC Spec Presentation**
   - System presents complete SPARC specification
   - Formatted for easy review (markdown, diagrams)
   - Side-by-side with original scope/value docs

2. **User Reviews**
   - Reads specification, pseudocode, architecture
   - Validates acceptance criteria
   - Checks technical feasibility
   - Identifies gaps or concerns

3. **User Decision**
   - **Option A: Approve** → Proceed to Phase 5 (development)
   - **Option B: Request Changes** → Return to Phase 3 with feedback
   - **Option C: Major Revision** → Return to Phase 2 (scope change)

4. **Approval Actions** (if approved)
   ```bash
   # System actions on approval
   - Store approved spec in AgentDB
   - Create acceptance-criteria.json (for validation)
   - Lock spec version (prevent changes during development)
   - Transition to development mode
   ```

5. **Output**
   - `.agentic/approved-specs/v1.0-approved.md`
   - `.agentic/approved-specs/acceptance-criteria.json` (used by Truth Verification)

---

## PHASE 5: London TDD Development with Continuous Swarm

**Duration**: Variable (4-40 hours, depends on scope)
**Participants**: HiveMind swarm (Queen, Collective Intelligence, Workers, Scouts, Memory Manager)
**Tools**: London TDD, AgentDB, Truth Verification, Pattern matching (optional)

### Workflow

```bash
# Launch TDD Swarm (runs continuously until complete)
.agentic/scripts/phase-5-develop.sh
```

### Continuous Development Loop

```
┌─────────────────────────────────────────────────────────────────┐
│ ITERATION LOOP (Continuous until all acceptance criteria pass) │
└─────────────────────────────────────────────────────────────────┘

1. QUEEN COORDINATOR: Reads approved spec from AgentDB
   ↓
2. QUEEN: Spawns worker swarm (8-10 workers)
   • Each worker assigned to specific acceptance criteria
   • Load balancing based on complexity
   ↓
3. WORKERS: London TDD Cycle (per worker, parallel)

   For each acceptance criterion assigned:

   [RED] Write failing test
   • Load acceptance criterion from spec
   • Write test that validates criterion
   • Mock dependencies (London School)
   • Run test → MUST FAIL (no implementation yet)
   • Report status to Memory Manager (30s)

   [GREEN] Implement minimal code to pass
   • Write simplest code that passes test
   • Optional: Vector search AgentDB for similar patterns
   • Run test → MUST PASS
   • Report status to Memory Manager (30s)

   [REFACTOR] Clean up with green tests
   • Improve code quality
   • Extract patterns
   • Run tests → MUST STAY GREEN
   • Report status to Memory Manager (30s)

   ↓
4. COLLECTIVE INTELLIGENCE: Continuous Validation (every 30s)
   • Check test coverage (>= 80% required)
   • Run Truth Verification (>= 0.95 threshold)
   • Validate architecture alignment
   • Check acceptance criteria progress
   • If validation fails → Auto-rollback + notify Queen
   • If validation passes → Workers continue
   ↓
5. SCOUT EXPLORERS: Research as needed
   • Find libraries/dependencies
   • Search for best practices
   • Optional: Find similar code patterns (AgentDB vector search)
   • Report findings to workers via Memory Manager
   ↓
6. SWARM MEMORY MANAGER: Coordination
   • Store worker status every 30s
   • Coordinate shared state (AgentDB)
   • Track test results
   • Track acceptance criteria completion
   ↓
7. QUEEN: Progress Monitoring
   • Every 30s: Check Memory Manager for worker status
   • Detect blocked workers → Reassign or spawn scouts
   • Detect completed criteria → Reallocate workers
   • Overall progress calculation:
     completion = completed_criteria / total_criteria
   ↓
8. LOOP until: ALL acceptance criteria pass + Truth Verification >= 0.95
   ↓
9. QUEEN: Final Validation
   • Run full test suite
   • Check Truth Verification (>= 0.95)
   • Validate all acceptance criteria (100% complete)
   • Check test coverage (>= 80%)
   • If all pass → Proceed to completion
   • If any fail → Return to iteration loop
   ↓
10. TRUTH VERIFICATION: Final Gate
    • Code correctness: >= 0.95 ✅
    • Test coverage: >= 80% ✅
    • Architecture alignment: verified ✅
    • Acceptance criteria: 100% ✅
    ↓
11. QUEEN: Create GitHub PR
    • Generate PR description (from spec + results)
    • Link to acceptance criteria
    • Include test coverage report
    • Include Truth Verification score
    • Mark as "Ready for Human Review"
    ↓
12. MEMORY MANAGER: Store as Pattern (Optional Learning)
    • If feature successful + high quality
    • Store in AgentDB patterns namespace
    • Make available for future vector search
    • System learns and improves
```

### Worker Coordination Protocol

**Every 30 seconds, each worker writes to AgentDB**:

```javascript
mcp__claude-flow__memory_usage({
  action: "store",
  key: `swarm/worker-${workerId}/status`,
  namespace: "coordination",
  value: JSON.stringify({
    worker_id: workerId,
    assigned_criterion: "AC-3: Generate valid OpenAPI spec",
    tdd_phase: "green", // red, green, refactor
    current_file: "src/openapi-generator.ts",
    tests_written: 12,
    tests_passing: 12,
    tests_failing: 0,
    coverage: 0.87,
    truth_score: 0.96,
    blocked: false,
    blockers: [],
    progress: 0.80, // 80% complete with assigned criterion
    timestamp: Date.now()
  })
});
```

**Queen reads all worker statuses every 30s**:

```javascript
// Check overall progress
const workerStatuses = await getAllWorkerStatuses(); // from AgentDB
const overallProgress = calculateProgress(workerStatuses);

if (overallProgress === 1.0) {
  // All criteria complete, run final validation
  await runFinalValidation();
} else {
  // Continue monitoring, reassign if needed
  await reallocateWorkersIfNeeded(workerStatuses);
}
```

### Truth Verification Integration

**Runs continuously during development**:

```javascript
// Every file write, validate
const truthScore = await verifyTruth({
  code: fileContents,
  tests: testFileContents,
  acceptanceCriteria: loadedFromSpec
});

if (truthScore < 0.95) {
  // Auto-rollback
  await gitRevertLastCommit();
  await notifyQueen({
    error: "Truth verification failed",
    score: truthScore,
    threshold: 0.95
  });
} else {
  // Continue
  await reportToMemoryManager({ truthScore });
}
```

### Pattern Reuse (Optional Optimization)

**Workers can optionally search for proven patterns**:

```javascript
// Before writing code, check for similar solutions
const patterns = await mcp__claude-flow__memory_usage({
  action: "search",
  pattern: "OpenAPI generation from code comments",
  namespace: "patterns"
});

if (patterns.found && patterns.similarity > 0.85) {
  // Reuse proven pattern (80-90% code reuse)
  const provenCode = await retrievePattern(patterns.result[0]);
  const adaptedCode = adaptToProjectContext(provenCode);
  // Still write tests first (TDD), but implementation is faster
}
```

---

## Post-Development: Human Review

**After Phase 5 completes**:

1. **GitHub PR Created**
   - Description: Spec + acceptance criteria + results
   - Tests: All passing, >= 80% coverage
   - Truth Score: >= 0.95
   - Status: "Ready for Human Review"

2. **User Reviews**
   - Code quality
   - Test coverage
   - Documentation
   - Architecture alignment

3. **User Decision**
   - **Approve & Merge**: Feature complete
   - **Request Changes**: Return to Phase 5 with feedback
   - **Reject**: Major issues, return to Phase 3 or 2

---

## Environment Setup

All 5 phases run in the same portable container:

- **Codespaces**: `.devcontainer/devcontainer.json`
- **Pi 5 / Local**: `docker-compose.yml`
- **Cloud**: Same `docker-compose.yml` → K8s

**One command setup**:

```bash
# From template repository
.agentic/scripts/setup.sh
```

---

## Summary

| Phase | Duration | Participants | Output | Gate |
|-------|----------|--------------|--------|------|
| 1: Research | 1-4 hours | User + Scouts | Research report, feasibility | None |
| 2: Formalize | 1-3 hours | User + Collective Intelligence | Scope, value prop, high-level arch | None |
| 3: SPARC Planning | 2-4 hours | SPARC agents | Formal spec, pseudocode, architecture | **User Approval** |
| 4: Approval | 15-60 min | User only | Approved spec, acceptance criteria | **User Approval** |
| 5: TDD Development | 4-40 hours | HiveMind swarm | Production code, tests, PR | **Truth Verification >= 0.95** |

**Total**: 8-51 hours from wild idea to production-ready code with human review gates.
