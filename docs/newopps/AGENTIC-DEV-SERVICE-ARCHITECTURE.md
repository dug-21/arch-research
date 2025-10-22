# Agentic Development Template - 5-Phase Creation Workflow

**Deployment**: Portable devcontainer.json + docker-compose.yml template
**Environments**: GitHub Codespaces, Raspberry Pi 5, Local Docker, Cloud
**Methodology**: Wild Idea → SPARC Planning → London TDD → Truth Verification
**Interface**: Claude Code with MCP integration
**Date**: 2025-10-21
**Version**: 4.0 (Portable 5-Phase Workflow Template)

---

## Executive Summary

A **repeatable, portable development workflow template** that takes you from wild idea to production-ready code through 5 structured phases. Works identically in GitHub Codespaces, on Raspberry Pi 5, local Docker, or cloud environments. Built on **SPARC methodology**, **London TDD**, **HiveMind swarm coordination**, and **Truth verification**.

### Your 5-Phase Creation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: Wild Idea + Deep Research                             │
│ • Brainstorm and discuss ideas                                  │
│ • Deep research with Goalie GOAP search                         │
│ • Web research, prior art analysis                              │
│ • Validate feasibility and novelty                              │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: Formalize Scope/Value + High-Level Architecture       │
│ • Iterate to full scope of the idea                             │
│ • Define value proposition                                      │
│ • Create high-level architecture definition                     │
│ • Identify key components and integrations                      │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 3: SPARC Planning                                         │
│ • Specification: Detailed requirements and constraints          │
│ • Pseudocode: Algorithm design and logic flow                   │
│ • Architecture: Technical design and component interaction      │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 4: Human Approval Checkpoint                              │
│ • Review SPARC specification                                    │
│ • Approve or request changes                                    │
│ • Gate before development begins                                │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 5: London TDD Development with Continuous Swarm          │
│ • Test-first development (London School TDD)                    │
│ • HiveMind swarm coordination (continuous iterations)           │
│ • Pattern-driven code reuse where applicable                    │
│ • Truth verification (≥0.95 threshold)                          │
│ • Iterate until completion                                      │
│ • Ready for human review                                        │
└─────────────────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **Portable Template**: Same workflow in Codespaces, Pi, Docker, Cloud
2. **5-Phase Flow**: Structured progression from idea to production
3. **Human Approval Gate**: Review before committing to development
4. **Continuous Swarm Iterations**: Development continues until completion
5. **Truth Verification**: Automated quality gate before human review
6. **Repeatable Setup**: devcontainer.json + scripts for instant setup

### Deployment Targets

| Environment | Setup | Use Case |
|-------------|-------|----------|
| **GitHub Codespaces** | `.devcontainer/devcontainer.json` | Cloud development, collaboration |
| **Raspberry Pi 5** | `docker-compose.yml` | Local hardware, always-on |
| **Local Docker** | `docker-compose.yml` | Development machine |
| **Cloud (AWS/GCP/Azure)** | `docker-compose.yml` → K8s | Production scaling |

### What Makes This Different

- **Not just a service**: A complete, portable development workflow template
- **5-phase structure**: From wild idea to verified production code
- **Pattern-driven is optional**: Used as optimization, not core architecture
- **Swarm coordination**: Continuous iterations during development phase
- **Truth verification**: Automated quality gate before human review
- **Works everywhere**: Same setup, different environments

---

## Template Architecture

### Repository Structure

```
my-project/
├── .devcontainer/
│   ├── devcontainer.json          # Codespaces/VS Code Dev Containers
│   ├── docker-compose.yml         # Dev environment orchestration
│   └── Dockerfile                 # Development container image
│
├── .agentic/
│   ├── agents/                    # 64+ agent definitions
│   │   ├── core/                  # researcher, coder, tester, reviewer
│   │   ├── hive-mind/             # queen, collective-intelligence, workers, scouts
│   │   ├── sparc/                 # spec, pseudocode, architect, refinement
│   │   └── tdd/                   # london-school TDD specialists
│   │
│   ├── config/
│   │   ├── phase-1-research.yml   # Goalie GOAP, web search config
│   │   ├── phase-2-formalize.yml  # Scope/value iteration config
│   │   ├── phase-3-sparc.yml      # SPARC methodology config
│   │   ├── phase-4-approval.yml   # Human checkpoint config
│   │   └── phase-5-tdd.yml        # London TDD + swarm config
│   │
│   ├── scripts/
│   │   ├── setup.sh               # One-command setup for any environment
│   │   ├── phase-1-research.sh    # Launch research agents
│   │   ├── phase-2-formalize.sh   # Launch formalization agents
│   │   ├── phase-3-sparc.sh       # Launch SPARC planning
│   │   ├── phase-4-approve.sh     # Human review checkpoint
│   │   └── phase-5-develop.sh     # Launch TDD swarm (continuous)
│   │
│   └── workflows/
│       └── 5-phase-template.yml   # Complete workflow definition
│
├── docker-compose.yml             # Production deployment (Pi, Cloud)
├── Dockerfile                     # Production container image
└── README.md                      # Setup instructions for template
```

### Container Architecture (Works Everywhere)

```
┌────────────────────────────────────────────────────────────────────┐
│  Environment: Codespaces / Pi 5 / Local Docker / Cloud            │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  Container: agentic-dev (12GB RAM recommended)               │ │
│  ├──────────────────────────────────────────────────────────────┤ │
│  │                                                               │ │
│  │  ┌────────────────────────────────────────────────────────┐  │ │
│  │  │ PHASE 1: RESEARCH (On-Demand)                          │  │ │
│  │  ├────────────────────────────────────────────────────────┤  │ │
│  │  │  🔍 Scout Explorers                                    │  │ │
│  │  │  • Goalie GOAP search (mcp__goalie__)                  │  │ │
│  │  │  • Web research, prior art analysis                    │  │ │
│  │  │  • AgentDB vector search for similar ideas             │  │ │
│  │  │  • Feasibility validation                              │  │ │
│  │  └────────────────────────────────────────────────────────┘  │ │
│  │                                                               │ │
│  │  ┌────────────────────────────────────────────────────────┐  │ │
│  │  │ PHASE 2: FORMALIZE (Iterative)                         │  │ │
│  │  ├────────────────────────────────────────────────────────┤  │ │
│  │  │  🧠 Collective Intelligence                            │  │ │
│  │  │  • Scope definition and iteration                      │  │ │
│  │  │  • Value proposition analysis                          │  │ │
│  │  │  • High-level architecture design                      │  │ │
│  │  │  • Component identification                            │  │ │
│  │  └────────────────────────────────────────────────────────┘  │ │
│  │                                                               │ │
│  │  ┌────────────────────────────────────────────────────────┐  │ │
│  │  │ PHASE 3: SPARC PLANNING (Formal)                       │  │ │
│  │  ├────────────────────────────────────────────────────────┤  │ │
│  │  │  📋 SPARC Agents                                       │  │ │
│  │  │  • Specification Agent (requirements, constraints)     │  │ │
│  │  │  • Pseudocode Agent (algorithm design, logic flow)     │  │ │
│  │  │  • Architecture Agent (technical design)               │  │ │
│  │  │  • Output: Formal SPARC specification                  │  │ │
│  │  └────────────────────────────────────────────────────────┘  │ │
│  │                                                               │ │
│  │  ┌────────────────────────────────────────────────────────┐  │ │
│  │  │ PHASE 4: HUMAN APPROVAL (Gate)                         │  │ │
│  │  ├────────────────────────────────────────────────────────┤  │ │
│  │  │  ✋ Approval Checkpoint                                │  │ │
│  │  │  • Present SPARC specification                         │  │ │
│  │  │  • Wait for human review                               │  │ │
│  │  │  • Collect feedback/changes                            │  │ │
│  │  │  • Iterate or proceed                                  │  │ │
│  │  └────────────────────────────────────────────────────────┘  │ │
│  │                                                               │ │
│  │  ┌────────────────────────────────────────────────────────┐  │ │
│  │  │ PHASE 5: LONDON TDD DEVELOPMENT (Continuous)           │  │ │
│  │  ├────────────────────────────────────────────────────────┤  │ │
│  │  │                                                         │  │ │
│  │  │  👑 QUEEN COORDINATOR                                  │  │ │
│  │  │  • Issues directives to worker swarm                   │  │ │
│  │  │  • Manages TDD iterations                              │  │ │
│  │  │  • Resource allocation                                 │  │ │
│  │  │  • Final PR creation                                   │  │ │
│  │  │                                                         │  │ │
│  │  │  🧠 COLLECTIVE INTELLIGENCE                            │  │ │
│  │  │  • Continuous validation (every 30s)                   │  │ │
│  │  │  • Truth verification (≥0.95 threshold)                │  │ │
│  │  │  • Pattern matching (optional optimization)            │  │ │
│  │  │  • Consensus on implementation decisions               │  │ │
│  │  │                                                         │  │ │
│  │  │  💾 SWARM MEMORY MANAGER                               │  │ │
│  │  │  • AgentDB (2-3ms queries, SQLite)                     │  │ │
│  │  │  • Coordination memory (hive mind state)               │  │ │
│  │  │  • Pattern storage (optional reuse)                    │  │ │
│  │  │  • Test results tracking                               │  │ │
│  │  │                                                         │  │ │
│  │  │  👷 WORKER SPECIALISTS (8-10 parallel)                 │  │ │
│  │  │  • LONDON TDD: Write tests FIRST                       │  │ │
│  │  │  • Mock dependencies (London School)                   │  │ │
│  │  │  • Implement to pass tests                             │  │ │
│  │  │  • Refactor with green tests                           │  │ │
│  │  │  • Report status every 30s                             │  │ │
│  │  │  • Continuous iterations until complete                │  │ │
│  │  │                                                         │  │ │
│  │  │  🔍 SCOUT EXPLORERS                                    │  │ │
│  │  │  • Research libraries/dependencies                     │  │ │
│  │  │  • Find similar code (optional pattern reuse)          │  │ │
│  │  │  • Validate best practices                             │  │ │
│  │  │                                                         │  │ │
│  │  │  ✅ TRUTH VERIFICATION                                 │  │ │
│  │  │  • Validate code correctness (≥0.95 threshold)         │  │ │
│  │  │  • Check test coverage (≥80%)                          │  │ │
│  │  │  • Verify architecture alignment                       │  │ │
│  │  │  • Gate before human review                            │  │ │
│  │  │                                                         │  │ │
│  │  └────────────────────────────────────────────────────────┘  │ │
│  │                                                               │ │
│  │  ┌────────────────────────────────────────────────────────┐  │ │
│  │  │ INTEGRATIONS                                           │  │ │
│  │  ├────────────────────────────────────────────────────────┤  │ │
│  │  │  • Claude Code MCP (87 tools)                          │  │ │
│  │  │  • Claude Agent SDK (foundation)                       │  │ │
│  │  │  • GitHub CLI (gh) - repository sync                   │  │ │
│  │  │  • Goalie MCP (GOAP search, web research)              │  │ │
│  │  │  • Truth Verification MCP                              │  │ │
│  │  │  • AgentDB (20 MCP tools, vector search)               │  │ │
│  │  └────────────────────────────────────────────────────────┘  │ │
│  │                                                               │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  Docker Volumes:                                                    │
│  • /workspace        - Project files (mounted from host/Codespaces)│
│  • /data/agentdb.db  - AgentDB database (persistent)               │
│  • /data/patterns    - Pattern library (optional, growing)         │
│  • /data/logs        - Execution logs                              │
│  • /root/.config/gh  - GitHub CLI authentication (persistent)      │
│                                                                     │
└────────────────────────────────────────────────────────────────────┘
```

### Why This Architecture Works

**Portable Template**:
- ✅ **Same devcontainer.json** works in Codespaces, VS Code, local Docker
- ✅ **Same docker-compose.yml** works on Pi, local machine, cloud
- ✅ **Same scripts** launch phases regardless of environment
- ✅ **No environment-specific code** - pure Docker abstraction

**5-Phase Flow**:
- ✅ **Phase 1-4**: On-demand agents (research, formalize, plan, approve)
- ✅ **Phase 5**: Continuous swarm (TDD iterations until complete)
- ✅ **Human gates**: Review at Phase 4 (approve spec) and end (review code)
- ✅ **Truth verification**: Automated quality gate before human review

**London TDD Integration**:
- ✅ **Test-first**: Workers write tests before implementation
- ✅ **Mock dependencies**: London School approach (fast, isolated)
- ✅ **Continuous iterations**: Swarm keeps working until tests pass
- ✅ **Pattern reuse optional**: Optimization, not requirement

**Swarm Coordination**:
- ✅ **HiveMind roles**: Queen, Collective Intelligence, Memory Manager, Workers, Scouts
- ✅ **Continuous communication**: Every 30s status updates via AgentDB
- ✅ **Parallel execution**: 8-10 workers simultaneously
- ✅ **Auto-healing**: Truth verification catches errors, auto-rollback

---

## 5-Phase Creation Workflow (Detailed)

### Your Complete Development Flow

**IMPORTANT**: This system is designed for **comprehensive, detailed specifications** - not sentence-level requests.

**User Provides**:
- Full feature requirements with acceptance criteria
- Edge cases and constraints
- Non-functional requirements (performance, security, etc.)
- Architecture preferences or constraints
- Examples or similar implementations

**Examples of Comprehensive Specs**:

✅ **Good** (Comprehensive):
```
Build OAuth2 authentication system with the following requirements:

Functional Requirements:
- Support Google and GitHub OAuth2 providers
- Use authorization code flow with PKCE
- Store tokens in Redis with 24h expiry
- Validate tokens on all protected routes

Non-Functional Requirements:
- Sub-50ms token validation latency
- Support 1000 concurrent sessions
- PII data encrypted at rest

Edge Cases:
- Handle expired tokens gracefully
- Support token refresh
- Handle provider API downtime

Architecture:
- Use passport.js for OAuth2 strategies
- Middleware-based token validation
- Reuse session management from repo-api-gateway if possible
```

❌ **Too Brief** (Won't work well):
```
"Add OAuth2 login"
```

---

## Pattern-Driven Development Workflow

### The Revolutionary Approach: Specs as Executable Patterns

```
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 1: PATTERN DISCOVERY (Scout Explorers)                    │
│ (Vector Search for Proven Implementations)                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│ User: [Provides comprehensive OAuth2 spec - see above]          │
│   ↓                                                              │
│ 🔍 SCOUT EXPLORERS: Vector Search AgentDB                       │
│   • Query: "OAuth2 authentication implementation"               │
│   • Search namespace: patterns/* (all proven patterns)          │
│   • Latency: 2-3ms semantic search                              │
│   ↓                                                              │
│ Results (ranked by similarity):                                  │
│   1. repo-A/patterns/oauth2-passport (similarity: 0.92)         │
│      → Proven: 94% test coverage, 0.97 truth score              │
│   2. repo-B/patterns/google-auth (similarity: 0.88)             │
│      → Proven: 87% test coverage, 0.96 truth score              │
│   3. proven-patterns/oauth2-pkce (similarity: 1.0)              │
│      → Proven: 100% test coverage, 0.98 truth score             │
│   ↓                                                              │
│ ✅ Output: 3 proven patterns with code references               │
└──────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 2: PATTERN SYNTHESIS (Collective Intelligence)            │
│ (Combine Best Practices from Proven Patterns)                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│ 🧠 COLLECTIVE INTELLIGENCE: Analyzes 3 proven patterns          │
│   • Extracts best practices from each                           │
│   • Combines architectural decisions                            │
│   • Generates acceptance criteria FROM patterns                 │
│   • Creates code references for reuse                           │
│   ↓                                                              │
│ Synthesized Pattern:                                             │
│   {                                                              │
│     pattern_id: "project-X-oauth2",                             │
│     required_components: [                                       │
│       { component: "passport-google", proven_in: "repo-A" },    │
│       { component: "pkce-flow", proven_in: "proven-patterns" }, │
│       { component: "redis-sessions", proven_in: "repo-A" }      │
│     ],                                                           │
│     acceptance_criteria: [                                       │
│       "Must implement PKCE (proven-patterns: 100% coverage)",   │
│       "Must use passport.js (repo-A: 94% coverage)",            │
│       "Must achieve >80% test coverage (pattern avg: 90%)"      │
│     ],                                                           │
│     code_references: {                                           │
│       "passport-google.js": "agentdb://repo-A/auth/...",        │
│       "pkce-utils.js": "agentdb://proven-patterns/..."          │
│     },                                                           │
│     expected_quality: { coverage: 0.90, truth_score: 0.95 }     │
│   }                                                              │
│   ↓                                                              │
│ 👑 QUEEN: Stores pattern in AgentDB                             │
│   • Namespace: patterns/project-X/oauth2                        │
│   • User reviews synthesized pattern                            │
│   • User approves → Pattern becomes executable spec             │
│   ↓                                                              │
│ ✅ Output: Executable pattern with 80-90% reusable code         │
└──────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 3: PATTERN-DRIVEN IMPLEMENTATION (Workers)                │
│ (Adapt Proven Code + Continuous Validation)                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│ 👑 QUEEN: Spawns workers for implementation                     │
│   ↓                                                              │
│ 👷 WORKERS: Load pattern from AgentDB (2ms)                     │
│   ↓                                                              │
│ For each required_component:                                     │
│   1. Vector search retrieves PROVEN CODE (2ms)                  │
│   2. Worker adapts code to project context (80% reuse)          │
│   3. Worker writes adapted code                                 │
│   4. IMMEDIATE pattern validation (2ms):                        │
│      • Compare to pattern.expected_quality                      │
│      • Pattern match score >= 0.85? Continue : Rollback         │
│   5. Report status to Queen via memory (30s intervals)          │
│   ↓                                                              │
│ Example (Google OAuth2 component):                              │
│   • Retrieved proven code from repo-A (2ms)                     │
│   • Adapted: Changed config, kept 85% of logic                  │
│   • Validated: Pattern match 0.91 ✅ (>= 0.85)                  │
│   • Stored: src/auth/passport-google.js                         │
│   ↓                                                              │
│ Every 30 seconds:                                                │
│   💾 MEMORY MANAGER: Validates ALL files against pattern        │
│   • Load pattern from AgentDB (2ms)                             │
│   • Validate each file (2ms per file)                           │
│   • Overall pattern match: 0.89 ✅                              │
│   • Auto-rollback if drops below 0.85 ❌                        │
│   ↓                                                              │
│ ✅ Output: Implementation with 80-90% proven code reuse         │
└──────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 4: CONTINUOUS VALIDATION (Collective Intelligence)        │
│ (Real-Time Pattern Matching + Truth Verification)               │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│ 🧠 COLLECTIVE INTELLIGENCE: Monitors workers every 30s          │
│   ↓                                                              │
│ Validation checks (all 2ms AgentDB queries):                     │
│   1. Pattern Match Score: 0.89 >= 0.85 ✅                       │
│   2. Test Coverage: 92% >= 80% ✅                               │
│   3. Truth Verification: 0.97 >= 0.95 ✅                        │
│   4. Acceptance Criteria:                                        │
│      • PKCE implemented ✅ (test passing)                       │
│      • passport.js used ✅ (code analysis)                      │
│      • Redis sessions ✅ (config verified)                      │
│   ↓                                                              │
│ IF any validation fails:                                         │
│   • Auto-rollback IMMEDIATELY (no waiting for milestones)       │
│   • Notify Queen → Issue directive to worker                    │
│   • Worker retries with different adaptation strategy           │
│   ↓                                                              │
│ IF all validations pass:                                         │
│   • Continue monitoring (validation is continuous)              │
│   • Workers proceed to next component                           │
│   ↓                                                              │
│ ✅ Output: Continuously validated implementation                │
└──────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│ PHASE 5: COMPLETION & LEARNING (Queen + Memory Manager)         │
│ (Final Validation + Store as New Pattern)                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│ 👷 WORKERS: Report completion to Queen                          │
│   ↓                                                              │
│ 👑 QUEEN: Final validation                                      │
│   • Load pattern from AgentDB (2ms)                             │
│   • Validate final code against ALL criteria                    │
│   • Pattern match: 0.91 ✅                                      │
│   • Truth score: 0.97 ✅                                        │
│   • All acceptance criteria: ✅                                 │
│   ↓                                                              │
│ IF validation passes:                                            │
│   • Create GitHub PR with compliance report                     │
│   • Wait for human merge approval                               │
│   • After merge: Store as NEW PATTERN                           │
│   ↓                                                              │
│ 💾 MEMORY MANAGER: Store successful implementation              │
│   • Save to: patterns/project-X/oauth2-complete                 │
│   • Update quality metrics: coverage 92%, truth 0.97            │
│   • Make available for future vector search                     │
│   • System learns and improves                                  │
│   ↓                                                              │
│ ✅ Output: Production-ready code + New pattern in library       │
└──────────────────────────────────────────────────────────────────┘
```

**Key Insight**: Orchestrator acts as **automated acceptance validator** - it's the gatekeeper ensuring implementation matches the approved spec. This requires tight coupling with AgentDB for instant spec retrieval and validation.

---

## Full Development Lifecycle (Detailed)

### Phase 1: Interactive Spec/Architecture Planning

**Goal**: Collaborate with AI agents to create comprehensive, approved specifications

**User Experience**: Highly interactive, iterative conversation with spec/architect agents

#### Step 1.1: Initial Feature Request
```
User: "I want to add OAuth2 authentication to the API"

Orchestrator:
  ✅ Detects: Feature request
  ✅ Initiates: Interactive planning mode
  ✅ Spawns: specification + system-architect + security-reviewer agents
  ✅ Sets mode: COLLABORATIVE (not autonomous)
```

#### Step 1.2: Interactive Specification Creation
```
┌─────────────────────────────────────────────────────────────┐
│ Specification Agent (Interactive Mode)                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Agent: "I'll help you create a specification for OAuth2    │
│         authentication. Let's start with requirements."     │
│                                                             │
│ Agent questions User (iterative):                          │
│   • Which OAuth2 flow? (authorization code, implicit, etc.)│
│   • Supported providers? (Google, GitHub, custom)          │
│   • Token storage? (JWT, database, Redis)                  │
│   • Session management strategy?                           │
│   • Required scopes/permissions?                           │
│                                                             │
│ User answers each question → Agent refines spec            │
│                                                             │
│ Agent generates DRAFT specification:                       │
│   ├─ Functional Requirements                               │
│   ├─ Non-Functional Requirements                           │
│   ├─ Acceptance Criteria (critical!)                       │
│   ├─ Edge Cases                                            │
│   ├─ Security Considerations                               │
│   └─ Testing Strategy                                      │
│                                                             │
│ User reviews DRAFT → Requests changes → Agent updates      │
│ (Iterates until user is satisfied)                         │
└─────────────────────────────────────────────────────────────┘
```

#### Step 1.3: Architecture Design (Still Interactive)
```
┌─────────────────────────────────────────────────────────────┐
│ System Architect Agent (Interactive Mode)                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Agent: "Based on the approved spec, I propose this         │
│         architecture for OAuth2 implementation..."          │
│                                                             │
│ Agent presents:                                             │
│   ├─ Component diagram (middleware, routes, services)      │
│   ├─ Data flow diagram (authorization → token → user)      │
│   ├─ Database schema (users, oauth_tokens, sessions)       │
│   ├─ API endpoints (/auth/login, /auth/callback, etc.)     │
│   └─ Dependencies (passport.js, jsonwebtoken, etc.)        │
│                                                             │
│ User reviews architecture → Provides feedback              │
│ Agent: "Should I use Redis for session storage or          │
│         database-backed sessions?"                          │
│ User: "Use Redis for performance"                          │
│ Agent: Updates architecture accordingly                    │
│                                                             │
│ Cross-repo pattern suggestion:                             │
│   Agent: "I found similar OAuth2 implementation in         │
│           repo-api-gateway with 92% match. Recommend        │
│           reusing the token validation middleware."         │
│   User: Approves reuse → Agent links pattern               │
└─────────────────────────────────────────────────────────────┘
```

#### Step 1.4: User Approval (Critical Milestone)
```
User: "This spec and architecture look good. Approved!"

Orchestrator:
  ✅ Marks spec as APPROVED
  ✅ Stores in AgentDB: repo-X/architecture/specs/oauth2-auth.md
  ✅ Creates acceptance criteria JSON:
     {
       "feature": "oauth2-authentication",
       "approvedBy": "user@example.com",
       "approvedAt": "2025-10-21T14:30:00Z",
       "acceptanceCriteria": [
         "Must support Google and GitHub OAuth2 providers",
         "Must use authorization code flow",
         "Tokens must be stored in Redis with 24h expiry",
         "Must implement PKCE for security",
         "Must have >80% test coverage",
         "Must validate tokens on every protected route"
       ],
       "architectureDecisions": [
         "Use passport.js for OAuth2 strategy",
         "Redis for session storage (performance)",
         "JWT for stateless token validation",
         "Reuse token validation middleware from repo-api-gateway"
       ]
     }
  ✅ Spec becomes SOURCE OF TRUTH for validation
  ✅ Transitions to: AUTOMATED DEVELOPMENT PHASE
```

**Key Point**: User has full control over spec/architecture. Nothing moves to development until user approves.

---

### Phase 2: Automated Development/Testing (Orchestrator as Validator)

**Goal**: Autonomously implement feature while validating against approved spec

**User Experience**: Hands-off - orchestrator manages everything, only notifies if validation fails

#### Step 2.1: TDD Swarm Initialization
```
Orchestrator (Autonomous Mode):
  ✅ Reads: Approved spec from AgentDB
  ✅ Parses: Acceptance criteria (becomes test assertions)
  ✅ Spawns: TDD London School swarm
     ├─ tester agent (writes failing tests first)
     ├─ coder agent (implements minimal code to pass)
     ├─ reviewer agent (validates code quality)
     └─ production-validator (checks deployment readiness)
  ✅ Sets validation rules:
     • Truth Verification: 0.95 threshold
     • Spec Compliance: 100% of acceptance criteria must pass
     • Test Coverage: >80% required
     • Architecture Alignment: Matches approved design
```

#### Step 2.2: Test-First Development (Automated)
```
┌─────────────────────────────────────────────────────────────┐
│ Tester Agent (Autonomous, Spec-Driven)                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Agent reads acceptance criteria from spec:                 │
│   "Must support Google and GitHub OAuth2 providers"        │
│                                                             │
│ Agent writes failing test:                                 │
│   describe('OAuth2 Authentication', () => {                │
│     it('should authenticate with Google provider', () => { │
│       // Test that Google OAuth2 flow works               │
│       expect(auth.supports('google')).toBe(true);         │
│     });                                                     │
│     it('should authenticate with GitHub provider', () => { │
│       expect(auth.supports('github')).toBe(true);         │
│     });                                                     │
│   });                                                       │
│                                                             │
│ Agent runs test: ❌ FAILS (as expected, no implementation) │
│                                                             │
│ Agent writes ALL tests for ALL acceptance criteria         │
│ (Test suite becomes executable version of spec)            │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Coder Agent (Autonomous, Test-Driven)                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Agent implements minimal code to pass tests:               │
│   class OAuth2Service {                                    │
│     supports(provider: string): boolean {                  │
│       return ['google', 'github'].includes(provider);      │
│     }                                                       │
│   }                                                         │
│                                                             │
│ Agent runs test: ✅ PASSES                                 │
│                                                             │
│ Agent continues with next failing test...                  │
│ (Red → Green → Refactor cycle)                             │
└─────────────────────────────────────────────────────────────┘
```

#### Step 2.3: Orchestrator Validation (Critical!)
```
┌─────────────────────────────────────────────────────────────┐
│ Orchestrator as Acceptance Validator                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Orchestrator performs multi-level validation:              │
│                                                             │
│ 1. Truth Verification (0.95 threshold):                    │
│    ├─ Code correctness: 0.97 ✅                            │
│    ├─ Logic soundness: 0.96 ✅                             │
│    └─ No hallucinations: verified ✅                       │
│                                                             │
│ 2. Spec Compliance (acceptance criteria):                  │
│    ├─ Supports Google OAuth2: ✅ (test passes)             │
│    ├─ Supports GitHub OAuth2: ✅ (test passes)             │
│    ├─ Uses authorization code flow: ✅ (verified)          │
│    ├─ Tokens in Redis with 24h TTL: ✅ (verified)          │
│    ├─ Implements PKCE: ✅ (verified)                       │
│    └─ Validates tokens on protected routes: ✅ (verified)  │
│                                                             │
│ 3. Test Coverage:                                           │
│    ├─ Unit tests: 87% ✅ (>80% required)                   │
│    ├─ Integration tests: 82% ✅                            │
│    └─ Edge case coverage: 91% ✅                           │
│                                                             │
│ 4. Architecture Alignment:                                  │
│    ├─ Uses passport.js: ✅ (as specified)                  │
│    ├─ Redis session storage: ✅ (as specified)             │
│    ├─ JWT tokens: ✅ (as specified)                        │
│    ├─ Reuses middleware from repo-api-gateway: ✅          │
│    └─ Follows approved component diagram: ✅               │
│                                                             │
│ 5. Security Validation:                                     │
│    ├─ No hardcoded secrets: ✅                             │
│    ├─ PKCE implementation correct: ✅                      │
│    ├─ Token expiry enforced: ✅                            │
│    └─ Input validation present: ✅                         │
│                                                             │
│ ALL VALIDATIONS PASSED ✅                                   │
│                                                             │
│ Orchestrator decision: APPROVED FOR MERGE                  │
└─────────────────────────────────────────────────────────────┘
```

#### Step 2.4: Auto-Rollback (If Validation Fails)
```
Example: Validation Failure Scenario

┌─────────────────────────────────────────────────────────────┐
│ Orchestrator Validation: FAILED ❌                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Spec Compliance Check:                                     │
│   ├─ Supports Google OAuth2: ✅                            │
│   ├─ Supports GitHub OAuth2: ✅                            │
│   ├─ Uses authorization code flow: ✅                      │
│   ├─ Tokens in Redis with 24h TTL: ❌ FAILED              │
│   │   → Found: Tokens stored in database, not Redis       │
│   │   → Spec required: Redis for performance              │
│   ├─ Implements PKCE: ❌ FAILED                            │
│   │   → PKCE implementation missing                       │
│   └─ Validates tokens: ✅                                  │
│                                                             │
│ VALIDATION FAILED: 2/6 acceptance criteria not met         │
│                                                             │
│ Orchestrator actions:                                       │
│   1. ❌ Auto-rollback all changes                          │
│   2. 📝 Generate deviation report                          │
│   3. 🔔 Notify user with details                           │
│   4. 🔁 Option: Re-spawn swarm with corrected instructions │
│                                                             │
│ User notification:                                          │
│   "Implementation failed validation against approved spec. │
│    Deviations:                                             │
│    • Token storage: Database used instead of Redis         │
│    • PKCE: Implementation missing                          │
│    Would you like me to retry with corrections?"           │
│                                                             │
│ User: "Yes, fix and retry"                                 │
│ Orchestrator: Re-spawns swarm with explicit corrections    │
└─────────────────────────────────────────────────────────────┘
```

#### Step 2.5: PR Creation (If Validation Passes)
```
Orchestrator (After Successful Validation):
  ✅ Creates GitHub PR with:
     ├─ Title: "feat: Add OAuth2 authentication (Google, GitHub)"
     ├─ Description: Links to approved spec in AgentDB
     ├─ Validation report:
     │   ├─ Truth Verification: 0.97/0.95 ✅
     │   ├─ Spec Compliance: 6/6 criteria met ✅
     │   ├─ Test Coverage: 87% ✅
     │   └─ Architecture Alignment: 100% ✅
     ├─ Test results: All tests passing
     └─ Recommendation: APPROVED FOR MERGE

  ✅ Requests code-review-swarm for final review
  ✅ Waits for human approval to merge
```

**Key Point**: Orchestrator is the gatekeeper. If implementation doesn't match spec, it auto-rollbacks. No human intervention needed unless validation fails.

---

### Orchestrator as Acceptance Validator: Implementation Details

**How does orchestrator validate spec compliance?**

```typescript
// Pseudocode: Orchestrator validation logic

class OrchestrationValidator {
  async validateImplementation(
    spec: ApprovedSpec,
    implementation: CodeChanges
  ): Promise<ValidationResult> {

    // 1. Load acceptance criteria from spec (AgentDB in-process query)
    const criteria = await agentdb.query({
      namespace: `repo-${spec.repo}/architecture/specs/`,
      key: spec.specId
    });

    // 2. Truth Verification (0.95 threshold)
    const truthScore = await truthVerifier.verify(implementation);
    if (truthScore < 0.95) {
      return {
        passed: false,
        reason: `Truth verification failed: ${truthScore} < 0.95`
      };
    }

    // 3. Run all tests (must pass)
    const testResults = await runner.runTests(implementation);
    if (!testResults.allPassed) {
      return {
        passed: false,
        reason: `Tests failed: ${testResults.failures}`
      };
    }

    // 4. Check test coverage (>80%)
    const coverage = testResults.coverage;
    if (coverage < 0.80) {
      return {
        passed: false,
        reason: `Coverage too low: ${coverage} < 0.80`
      };
    }

    // 5. Validate each acceptance criterion
    for (const criterion of criteria.acceptanceCriteria) {
      const met = await this.checkCriterion(criterion, implementation);
      if (!met) {
        return {
          passed: false,
          reason: `Acceptance criterion not met: ${criterion}`
        };
      }
    }

    // 6. Validate architecture alignment
    const architectureValid = await this.checkArchitecture(
      criteria.architectureDecisions,
      implementation
    );
    if (!architectureValid.passed) {
      return {
        passed: false,
        reason: `Architecture deviation: ${architectureValid.deviation}`
      };
    }

    // All validations passed
    return { passed: true };
  }

  // Check individual acceptance criterion
  async checkCriterion(
    criterion: string,
    implementation: CodeChanges
  ): Promise<boolean> {
    // Example: "Must support Google OAuth2 provider"

    // 1. Parse criterion into testable assertion
    const assertion = this.parseCriterion(criterion);

    // 2. Find corresponding test
    const test = implementation.tests.find(t =>
      t.description.includes(assertion.keyword)
    );

    // 3. Verify test exists and passes
    if (!test || !test.passed) return false;

    // 4. Verify implementation actually satisfies criterion
    const codeAnalysis = await this.analyzeCode(
      implementation.code,
      assertion
    );

    return codeAnalysis.satisfies;
  }
}
```

**Why tight coupling with AgentDB is critical**:
- Orchestrator needs **instant access** to approved specs (no HTTP latency)
- Validation happens **per-agent-action** (not just at end)
- Spec queries are **frequent** (every code change checked against criteria)
- In-process AgentDB: `agentdb.query()` = function call (2-3ms)
- Separate container: HTTP request (10-50ms + network overhead)

---

## Docker Compose Configuration

### Pattern-Driven Single Container (Recommended)

```yaml
# docker-compose.yml (Pattern-Driven Development with HiveMind)
version: '3.8'

services:
  # Pattern-Driven Development: HiveMind + AgentDB + GitHub
  pattern-dev:
    image: agentic-dev/pattern-driven:latest
    container_name: pattern-orchestrator
    build:
      context: ./services/pattern-dev
      dockerfile: Dockerfile
    environment:
      - NODE_ENV=production

      # AgentDB Configuration (In-Process)
      - AGENTDB_ENABLED=true
      - AGENTDB_PATH=/data/agentdb.db
      - AGENTDB_VECTOR_SEARCH_ENABLED=true

      # HiveMind Coordination
      - HIVEMIND_ENABLED=true
      - ENABLE_QUEEN_COORDINATOR=true
      - ENABLE_COLLECTIVE_INTELLIGENCE=true
      - ENABLE_MEMORY_MANAGER=true
      - ENABLE_WORKER_SPECIALISTS=true
      - ENABLE_SCOUT_EXPLORERS=true

      # Pattern-Driven Features
      - ENABLE_PATTERN_MATCHING=true
      - ENABLE_CONTINUOUS_VALIDATION=true
      - PATTERN_MATCH_THRESHOLD=0.85
      - TRUTH_VERIFICATION_THRESHOLD=0.95

      # GitHub Integration (Native gh CLI)
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - ENABLE_GITHUB_SYNC=true

      # API Keys
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

      # Parallel Capacity
      - MAX_PARALLEL_PROJECTS=10

    volumes:
      # AgentDB Data (Patterns + Coordination + Repos)
      - agentdb-data:/data

      # GitHub Clones
      - repos-data:/repos

      # Agent Definitions (64+, read-only)
      - agent-definitions:/app/agents:ro

      # Proven Patterns Library (read-only)
      - proven-patterns:/patterns:ro

      # Secrets (in-process vault)
      - secrets:/app/secrets

      # Logs
      - logs:/app/logs

    networks:
      - external-apis

    ports:
      - "3000:3000"  # MCP server
      - "3001:3001"  # AgentDB monitoring API

    restart: unless-stopped

    # Resource Limits (16GB Pi 5)
    mem_limit: 12g  # 12GB for pattern-driven development
    cpus: 3.0       # 3 cores (leave 1 for system)

    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

networks:
  external-apis:
    driver: bridge

volumes:
  # AgentDB Database (up to 50GB)
  agentdb-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /mnt/storage/agentdb-data

  # GitHub Repository Clones
  repos-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /mnt/storage/repos

  # Agent Definitions (64+ .md files)
  agent-definitions:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /mnt/storage/agents

  # Proven Patterns Library (read-only)
  proven-patterns:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /mnt/storage/proven-patterns

  # Encrypted Secrets Vault
  secrets:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /mnt/storage/secrets

  # Application Logs
  logs:
    driver: local
```

### Why Pattern-Driven Single Container?

**Performance Benefits**:
1. ✅ **2ms pattern matching**: AgentDB in-process (vs 50-100ms HTTP)
2. ✅ **No network overhead**: HiveMind roles as threads, not containers
3. ✅ **Instant validation**: Pattern matching every 30s with 2ms queries
4. ✅ **Direct memory sharing**: Queen ↔ Workers ↔ Memory Manager

**Development Benefits**:
5. ✅ **80-90% code reuse**: Vector search finds proven implementations
6. ✅ **4x faster development**: Adapt patterns vs code from scratch
7. ✅ **4-10x fewer bugs**: Reuse tested, validated patterns
8. ✅ **100% consistency**: All code follows architectural patterns

**Operational Benefits**:
9. ✅ **Simple debugging**: Single log stream, unified monitoring
10. ✅ **Less resource consumption**: One base OS layer
11. ✅ **8-10 parallel projects**: 12GB RAM supports multiple simultaneous developments

### Resource Allocation (16GB Pi 5)

```yaml
# Resource distribution for 16GB Pi 5:
Total RAM: 16GB
├── pattern-dev container: 12GB
│   ├── HiveMind Coordination: 4-5GB
│   │   ├── Queen Coordinator (1GB)
│   │   ├── Collective Intelligence (1.5GB)
│   │   ├── Memory Manager (1GB)
│   │   └── Scout Explorers (0.5GB)
│   ├── Worker Specialists: 5-6GB
│   │   └── 8-10 parallel workers (500-600MB each)
│   ├── AgentDB In-Process: 2-3GB
│   │   ├── SQLite database (patterns)
│   │   ├── Vector search cache
│   │   └── Coordination memory
│   └── Native integrations: <1GB
│       ├── GitHub CLI (gh)
│       ├── Secret vault
│       └── MCP server
├── System + Docker: 2GB
│   ├── Raspberry Pi OS
│   └── Docker daemon
├── Free buffer: 2GB
│   └── Burst capacity for peak loads
└── Total: 16GB

# With 12GB allocated, can run:
# - 8-10 parallel pattern-driven projects
# - Each project: 500-600MB RAM
# - Continuous pattern validation (2ms)
# - Real-time HiveMind coordination
```

---

## Quality & Consistency Improvements

### Pattern-Driven vs Traditional Development

| Metric | Traditional (Document-Driven) | Pattern-Driven (This System) | Improvement |
|--------|------------------------------|------------------------------|-------------|
| **Development Speed** | 4-8 hours (from scratch) | 1-2 hours (adapt patterns) | **4x faster** |
| **Code Reuse** | 10-20% (manual copy-paste) | 80-90% (vector search) | **4-8x more reuse** |
| **Bug Rate** | 10-20% (new code) | 2-5% (proven patterns) | **4-10x fewer bugs** |
| **Validation Latency** | 50-100ms (HTTP/network) | 2ms (AgentDB in-process) | **25-50x faster** |
| **Consistency** | Variable (developer-dependent) | 100% (pattern-driven) | **Perfect consistency** |
| **Quality Checks** | Manual (end of phase) | Automatic (every 30s) | **Continuous** |
| **Learning** | None (siloed projects) | Automatic (vector database) | **Infinite improvement** |
| **Test Coverage** | 60-70% typical | 80-95% (from patterns) | **+20-35%** |
| **Architecture Alignment** | Manual review | Automatic pattern matching | **100% compliance** |

### How Pattern-Driven Achieves Superior Quality

**1. Start with Proven Solutions** (Not Blank Slate)
```
Traditional:
  User spec → Agents code from scratch → High bug risk

Pattern-Driven:
  User spec → Vector search (2ms) → Find 3 proven patterns →
  Combine best practices → Adapt 80-90% proven code → Low bug risk
```

**2. Continuous Validation** (Not End-of-Phase)
```
Traditional:
  Code complete → Run validation → Wait for results (50-100ms) →
  Find bugs → Rollback → Rework

Pattern-Driven:
  Every 30 seconds:
    - Pattern match validation (2ms)
    - Auto-rollback IMMEDIATELY if deviation
    - No wasted work, no late discoveries
```

**3. Learning System** (Not Static)
```
Traditional:
  Project complete → Knowledge lost → Next project starts from scratch

Pattern-Driven:
  Project complete → Store as pattern → Update quality metrics →
  Future projects find this pattern (2ms) → Quality compounds
```

### Expected Outcomes

**After 10 Projects**:
- Pattern library contains 10 proven implementations
- Future projects find 80-90% code reusable
- Development time: 1-2 hours (vs 4-8 hours)
- Bug rate: 2-5% (vs 10-20%)

**After 50 Projects**:
- Pattern library contains 50 proven implementations
- Vector search returns high-similarity matches (0.90+)
- Development time: 30-60 minutes (adapt near-identical patterns)
- Bug rate: 1-2% (proven patterns refined over time)

**After 100 Projects**:
- Pattern library is comprehensive for domain
- Most new projects are 95%+ pattern reuse
- Development time: 15-30 minutes (minor customization)
- Bug rate: <1% (battle-tested patterns)
- **Quality improves exponentially**

---

## Component Mapping to Requirements

### 1. Memory Architecture - AgentDB + Namespace Isolation

**Component**: AgentDB (from research: 11-agentdb.md, 02-claude-flow.md)

#### Central AgentDB Instance
```
Single SQLite Database on Pi 5:
├── Namespace: "central/*"               (Indefinite persistence)
│   ├── architecture-patterns/*
│   ├── best-practices/*
│   ├── cross-repo-learnings/*
│   └── validated-solutions/*
│
├── Namespace: "repo-{name}/*"           (Hybrid TTL)
│   ├── architecture/*                   (Persist: repo lifetime)
│   ├── experiments/*                    (TTL: 30 days)
│   ├── decisions/*                      (Persist: repo lifetime)
│   └── session-context/*                (TTL: 7 days)
│
├── Namespace: "research/*"              (Organized by issue)
│   ├── issue-{number}/*                 (TTL: 90 days)
│   │   ├── findings/*
│   │   ├── citations/*
│   │   └── synthesis/*
│
└── Namespace: "active-swarm-{id}/*"     (Ephemeral: session only)
    ├── current-context/*
    ├── agent-coordination/*
    └── task-state/*
```

**Isolation Strategy**:
- Each active swarm gets ephemeral namespace
- Swarm can only read from:
  - Its own ephemeral namespace
  - Specific repo namespace (if working on that repo)
  - Central namespace (read-only for patterns)
- Prevents cross-contamination via strict namespace ACLs

**Performance**: 2-3ms semantic search, sub-millisecond retrieval

---

### 2. Development Methodology - SPARC → TDD → Truth Verification

**Components**:
- claude-flow SPARC skills (02-claude-flow.md)
- tdd-london-swarm (02-claude-flow.md)
- Truth Verification System (02-claude-flow.md)

#### Workflow Pipeline

```
┌────────────────────────────────────────────────────────────┐
│ PHASE 1: SPARC Specification                               │
├────────────────────────────────────────────────────────────┤
│ Agents: specification, researcher, system-architect         │
│ Output: .agentic-dev/specs/{feature}.md                    │
│ Stored: repo-{name}/architecture/specs                     │
│ Duration: ~5-15 minutes                                     │
└────────────────────────────────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────┐
│ PHASE 2: SPARC Pseudocode                                  │
├────────────────────────────────────────────────────────────┤
│ Agents: pseudocode, coder, system-architect                │
│ Output: .agentic-dev/pseudocode/{feature}.md               │
│ Stored: repo-{name}/architecture/algorithms                │
│ Duration: ~10-20 minutes                                    │
└────────────────────────────────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────┐
│ PHASE 3: SPARC Architecture                                │
├────────────────────────────────────────────────────────────┤
│ Agents: architecture, system-architect, backend-dev        │
│ Output: .agentic-dev/architecture/{feature}.md             │
│ Stored: repo-{name}/architecture/designs                   │
│ Duration: ~15-30 minutes                                    │
└────────────────────────────────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────┐
│ PHASE 4: TDD London School (Test-First)                   │
├────────────────────────────────────────────────────────────┤
│ Agents: tdd-london-swarm, tester                           │
│ Process:                                                    │
│  1. Write failing test (mocks/stubs)                       │
│  2. Implement minimal code to pass                         │
│  3. Refactor                                               │
│  4. Repeat                                                 │
│ Output: tests/* + src/*                                    │
│ Stored: repo-{name}/experiments/{feature}-tdd              │
│ Duration: ~30-60 minutes                                    │
└────────────────────────────────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────┐
│ PHASE 5: Truth Verification (0.95 threshold)              │
├────────────────────────────────────────────────────────────┤
│ Agents: truth-verification, reviewer, production-validator │
│ Checks:                                                     │
│  • Code correctness (>95% accuracy score)                  │
│  • Test coverage (>80%)                                    │
│  • Architecture compliance (matches SPARC design)          │
│  • Security validation (no vulnerabilities)                │
│ Action: Auto-rollback if <95% OR proceed to merge         │
│ Stored: repo-{name}/decisions/validations                 │
│ Duration: ~5-10 minutes                                     │
└────────────────────────────────────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────┐
│ PHASE 6: SPARC Refinement & Completion                    │
├────────────────────────────────────────────────────────────┤
│ Agents: refinement, code-review-swarm                      │
│ Actions:                                                    │
│  • Performance optimization                                │
│  • Documentation generation                                │
│  • CI/CD pipeline integration                              │
│  • GitHub PR creation                                      │
│ Stored: central/architecture-patterns (if validated)       │
│ Duration: ~15-30 minutes                                    │
└────────────────────────────────────────────────────────────┘
```

**Total Estimated Time**: 1.5-3 hours per feature (end-to-end)

---

### 3. Research Mode - Read-Only, Multi-Agent, GOAP + FACT

**Components**:
- GOAP System (goal-oriented action planning) - 02-claude-flow.md
- FACT (tool-based retrieval) - 04-FACT.md
- Multi-agent research swarms - 02-claude-flow.md
- scout-explorer, researcher, analyst agents - 02-claude-flow.md

#### Research Workflow

```
┌────────────────────────────────────────────────────────────┐
│ Research Project: Tracked via GitHub Issue #N              │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ 1. Issue Created → Auto-spawns research swarm              │
│    Agents: scout-explorer, researcher, analyst             │
│    Namespace: research/issue-{N}/*                         │
│    Access: Read-only to all code repos                     │
│                                                             │
│ 2. GOAP Planning                                           │
│    • Goal decomposition (research objectives)              │
│    • Action sequencing (search → analyze → synthesize)     │
│    • Dynamic replanning based on findings                  │
│                                                             │
│ 3. FACT Integration (Tool-Based Retrieval)                 │
│    • SQL queries (if analyzing existing data)              │
│    • API calls (external research sources)                 │
│    • Schema introspection (understand code architecture)   │
│    • Multi-tier caching (avoid redundant searches)         │
│                                                             │
│ 4. Multi-Agent Coordination                                │
│    • scout-explorer: Find relevant sources                 │
│    • researcher: Deep analysis of sources                  │
│    • analyst: Synthesize findings                          │
│    • code-analyzer: Read-only code pattern analysis        │
│                                                             │
│ 5. Output Generation                                       │
│    Format: Markdown with citations                         │
│    Location: research-repo/issues/{N}/findings.md          │
│    Sections:                                               │
│      • Executive Summary                                   │
│      • Detailed Analysis                                   │
│      • Synthesis & Recommendations                         │
│      • Citations & References                              │
│      • Next Steps → Development Project                    │
│                                                             │
│ 6. Knowledge Transfer                                      │
│    • Store findings → research/issue-{N}/validated         │
│    • If applicable → central/architecture-patterns          │
│    • Link to development issue (GitHub issue linking)      │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

**Read-Only Access Implementation**:
```yaml
# Research swarm permissions
permissions:
  code_repos:
    read: true
    write: false
    execute: false
  research_repo:
    read: true
    write: true  # Only to issues/{N}/ directory
  agentdb:
    namespace: research/issue-{N}/*
    ttl: 90 days
```

---

### 4. Cross-Repo Capabilities - Module Referencing & Knowledge Transfer

**Components**:
- AgentDB cross-namespace search (11-agentdb.md)
- Pattern suggestion system (02-claude-flow.md)
- Multi-repo coordination (02-claude-flow.md)

#### Module Referencing System

**Scenario**: Building new API in Repo B, needs to reference authentication module from Repo A

```
┌────────────────────────────────────────────────────────────┐
│ Swarm Working on Repo B (new API)                          │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ 1. Agent identifies need for authentication                │
│                                                             │
│ 2. Query AgentDB across namespaces:                        │
│    SELECT * FROM memories                                  │
│    WHERE namespace IN (                                    │
│      'central/architecture-patterns/*',                    │
│      'repo-A/architecture/*'                               │
│    )                                                       │
│    AND content SIMILAR TO 'API authentication pattern'     │
│    LIMIT 10                                                │
│                                                             │
│ 3. Results:                                                │
│    • central/architecture-patterns/auth-best-practices     │
│    • repo-A/architecture/auth-module-design                │
│    • repo-A/decisions/oauth2-implementation                │
│                                                             │
│ 4. Agent analyzes Repo A's actual code (read-only):        │
│    • Understands interface/API of auth module              │
│    • Identifies dependencies                               │
│    • Extracts usage patterns                               │
│                                                             │
│ 5. Recommendation to developer:                            │
│    "I found a validated authentication pattern in Repo A.  │
│     Options:                                               │
│     1. Reference Repo A as dependency (if shared library)  │
│     2. Replicate pattern in Repo B (if independent)        │
│     3. Extract to shared library (if not already)"         │
│                                                             │
│ 6. Developer decision captured:                            │
│    Stored → repo-B/decisions/auth-approach                 │
│    Links → repo-A/architecture/auth-module (reference)     │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

#### Automatic Pattern Suggestion

**Trigger**: New feature request in any repo
**Process**:
1. Semantic search across `central/architecture-patterns/*`
2. Find similar features built in other repos
3. Surface to swarm with confidence score
4. Swarm decides: adopt, adapt, or ignore

**Example**:
```
User: "Build a rate limiter for the new API"

Swarm finds:
  • repo-C/architecture/rate-limiter-design (confidence: 0.92)
  • central/architecture-patterns/rate-limiting (confidence: 0.88)

Swarm suggests:
  "Found validated rate limiter in Repo C (92% match).
   Implementation uses token bucket algorithm with Redis.
   Estimated time savings: 70% if pattern reused.
   Recommend: Review and adapt for current API."
```

---

### 5. GitHub Integration - Auto-Sync, Secrets, Issue Management

**Components**:
- GitHub Integration System (6 modes) - 02-claude-flow.md
- issue-tracker agent - 02-claude-flow.md
- pr-manager agent - 02-claude-flow.md
- workflow-automation agent - 02-claude-flow.md

#### GitHub Sync Engine

```typescript
// Conceptual architecture
class GitHubSyncEngine {
  // Repository Discovery
  async discoverRepositories(token: string, org: string) {
    // Fetch all repos from GitHub org/user
    // Filter by criteria (public/private, topics, etc.)
    // Auto-register in AgentDB catalog
  }

  // Auto-Sync Process (runs every 5 minutes)
  async syncRepositories() {
    for (const repo of registeredRepos) {
      // 1. Fetch latest commits
      // 2. Sync issues → research/issue-{N}/* namespace
      // 3. Sync PRs → track in AgentDB
      // 4. Update local clone (git pull)
      // 5. Trigger hooks if configured
    }
  }

  // Secret Management (Centralized)
  async getSecret(repo: string, key: string): Promise<string> {
    // Retrieve from encrypted vault
    // Namespace: secrets/repo-{name}/{key}
    // Encryption: AES-256-GCM (from QuDAG)
    // Access control: Least privilege per repo
  }

  // Issue Management
  async handleIssueEvent(issue: GitHubIssue) {
    if (issue.labels.includes('research')) {
      // Spawn research swarm
      await spawnResearchSwarm(issue.number, issue.body);
    } else if (issue.labels.includes('feature')) {
      // Trigger SPARC workflow
      await initiateSPARCWorkflow(issue.number, issue.body);
    }
  }
}
```

#### Secret Management Architecture

```
┌────────────────────────────────────────────────────────────┐
│ Centralized Secret Vault (on Pi 5)                         │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ Encryption: AES-256-GCM (QuDAG component)                  │
│ Storage: SQLite (separate from AgentDB)                    │
│                                                             │
│ Structure:                                                  │
│   secrets/                                                  │
│   ├── global/                                              │
│   │   ├── github-token (encrypted)                         │
│   │   ├── anthropic-api-key (encrypted)                    │
│   │   └── openrouter-api-key (encrypted)                   │
│   │                                                         │
│   ├── repo-A/                                              │
│   │   ├── database-password (encrypted)                    │
│   │   ├── aws-access-key (encrypted)                       │
│   │   └── api-secret (encrypted)                           │
│   │                                                         │
│   └── repo-B/                                              │
│       ├── stripe-api-key (encrypted)                       │
│       └── sendgrid-api-key (encrypted)                     │
│                                                             │
│ Access Control:                                             │
│   • Swarm working on Repo A → can ONLY access repo-A/* keys│
│   • All swarms → read global/* keys                        │
│   • No cross-repo secret access                            │
│                                                             │
│ Audit Trail:                                                │
│   • Every secret access logged                             │
│   • Timestamp, swarm ID, repo, key name                    │
│   • Stored in AgentDB: central/audit-trail/*               │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

#### CI/CD Integration

**Component**: workflow-automation agent (02-claude-flow.md)

**Capabilities**:
1. **Auto-generate GitHub Actions workflows**
   - On repo initialization
   - Based on detected stack (Node.js, Python, etc.)
   - Stored in `.github/workflows/`

2. **Hooks integration**
   ```yaml
   # Example: .agentic-dev.yaml
   hooks:
     pre-commit:
       - lint
       - type-check
       - test-unit
     pre-push:
       - test-integration
     post-merge:
       - deploy-preview (if staging branch)
   ```

3. **PR automation**
   - Auto-create PRs after SPARC completion
   - Request code-review-swarm analysis
   - Auto-label based on changes

---

### 6. Swarm Coordination - Adaptive Topology

**Component**: claude-flow Swarm System (02-claude-flow.md)

#### Topology Selection Logic

```typescript
function selectTopology(task: Task): SwarmTopology {
  // Simple heuristics (can be enhanced with ML)

  if (task.type === 'research') {
    // Research benefits from parallel exploration
    return 'mesh'; // Peer-to-peer for scout-explorer agents
  }

  if (task.complexity === 'high' && task.repos.length > 1) {
    // Multi-repo complex task needs coordination
    return 'hierarchical'; // Queen-led for orchestration
  }

  if (task.type === 'development' && task.agents.length <= 5) {
    // Small dev tasks with few agents
    return 'star'; // Centralized coordination (efficient)
  }

  if (task.duration > '2 hours') {
    // Long-running tasks need adaptability
    return 'adaptive'; // Switches topology as needed
  }

  // Default: balanced approach
  return 'mesh';
}
```

#### Swarm Lifecycle

```
1. Spawn → Initialize namespace, load context from AgentDB
2. Plan → GOAP or SPARC planning phase
3. Execute → Agents work in parallel/sequential as needed
4. Coordinate → Real-time agent communication via hooks
5. Validate → Truth verification (if development)
6. Persist → Store learnings to AgentDB
7. Cleanup → Clear ephemeral namespace, archive metrics
```

---

### 7. Agent Roster - All 64+ Available

**Storage**: All agent definitions are markdown files on disk (`.claude/agents/`)

**Loading**: Dynamic agent spawning based on task requirements

**Categories** (from 02-claude-flow.md):
- Core Development (5): coder, reviewer, tester, planner, researcher
- SPARC Methodology (6): sparc-coord, specification, pseudocode, architecture, refinement, sparc-coder
- Specialized Development (6): backend-dev, mobile-dev, ml-developer, cicd-engineer, api-docs, system-architect
- Swarm Coordination (5): hierarchical-coordinator, mesh-coordinator, adaptive-coordinator, etc.
- GitHub Management (8): pr-manager, code-review-swarm, issue-tracker, release-manager, etc.
- Research (3): scout-explorer, researcher, analyst
- Distributed Systems (7): consensus, Byzantine, etc.
- Performance (6): perf-analyzer, benchmarker, etc.
- And 18+ more...

**No restrictions** - all agents available, swarm intelligently selects based on task

---

### 8. Cost Tracking & Optimization

**Components**:
- Multi-Model Router (01-agentic-flow.md) - 85-99% savings
- Agent Booster (01-agentic-flow.md) - 352x faster, $0 cost local execution
- token_usage tracking (02-claude-flow.md)

#### Cost Architecture

```
┌────────────────────────────────────────────────────────────┐
│ Cost Tracking System                                        │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ Per-Repo Tracking:                                         │
│   costs/                                                    │
│   ├── repo-A/                                              │
│   │   ├── total: $X.XX                                     │
│   │   ├── breakdown:                                       │
│   │   │   ├── api-calls: $X.XX                             │
│   │   │   ├── tokens-used: XXXXX                           │
│   │   │   └── local-compute: $0.00                         │
│   │   └── history: [{timestamp, task, cost}]              │
│   │                                                         │
│   └── repo-B/ ...                                          │
│                                                             │
│ Global Cap:                                                 │
│   total_budget: $XXX.XX per month                          │
│   current_spend: $X.XX                                     │
│   remaining: $XXX.XX                                        │
│   alert_threshold: 80% ($XXX.XX)                           │
│                                                             │
│ Optimization Strategy:                                      │
│   1. Local-first (Pi 5):                                   │
│      • AgentDB queries (2-3ms, $0)                         │
│      • Code analysis (read-only, $0)                       │
│      • Simple planning ($0)                                │
│                                                             │
│   2. Hybrid (Pi 5 + Cloud):                                │
│      • Heavy swarms (10+ agents) → Cloud workers           │
│      • Complex reasoning → Claude API (via Multi-Model)    │
│      • Parallel tasks → Distributed execution              │
│                                                             │
│   3. Multi-Model Router:                                   │
│      • Route simple queries → local ONNX models            │
│      • Route complex reasoning → Claude Sonnet 4           │
│      • Route bulk operations → cheaper providers           │
│      • 85-99% cost savings vs Claude-only                  │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

### 9. Security - Post-Quantum, Zero-Trust, Namespace Isolation

**Components**:
- QuDAG (post-quantum crypto) - 07-qudag.md
- Zero-trust architecture - 05-daa.md, 07-qudag.md
- Namespace isolation - 11-agentdb.md

#### Security Architecture

```
┌────────────────────────────────────────────────────────────┐
│ Security Layers                                             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│ 1. Post-Quantum Cryptography (QuDAG)                       │
│    • ML-KEM-768: Key encapsulation (NIST Level 3)          │
│    • ML-DSA: Digital signatures (quantum-resistant)        │
│    • HQC: Code-based encryption                            │
│    • Used for: Secret vault, sensitive memory              │
│                                                             │
│ 2. Zero-Trust Architecture                                 │
│    Principles:                                              │
│      • Never trust, always verify                          │
│      • Least privilege access                              │
│      • Continuous authentication                           │
│                                                             │
│    Implementation:                                          │
│      • Every swarm action verified                         │
│      • Namespace ACLs enforced                             │
│      • Secret access audited                               │
│      • No implicit trust between repos                     │
│                                                             │
│ 3. Namespace Isolation (AgentDB)                           │
│    • Swarm A cannot access Swarm B's namespace             │
│    • Repo-specific namespaces strictly isolated            │
│    • Cross-namespace queries require explicit permission   │
│    • Ephemeral namespaces auto-deleted after session       │
│                                                             │
│ 4. Centralized API Key Management                          │
│    • All keys encrypted (AES-256-GCM)                      │
│    • Least privilege per repository                        │
│    • Audit trail for every access                          │
│    • Keys never exposed in logs/memory dumps               │
│                                                             │
│ 5. Network Security (Minimal)                              │
│    • No special firewall rules required                    │
│    • GitHub access via HTTPS only                          │
│    • MCP communication via stdio (local)                   │
│    • Cloud workers via encrypted QUIC (optional)           │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

### 10. Configuration - Opinionated Defaults + Local Repo Config

#### Repository Configuration File

**Location**: `.agentic-dev.yaml` (in repo root)

```yaml
# .agentic-dev.yaml - Minimal, opinionated configuration

# Repository identity
repo:
  name: my-api-project
  type: development  # or "research"

# Methodology (defaults applied if not specified)
methodology:
  development: sparc  # Specification → Pseudocode → Architecture → Refinement
  testing: tdd-london  # Mock-driven TDD
  validation: truth-verification  # 0.95 accuracy threshold

# Memory configuration
memory:
  persistence:
    architecture: repo-lifetime  # Persists indefinitely
    experiments: 30d  # TTL: 30 days
    decisions: repo-lifetime
    session: 7d  # TTL: 7 days
  namespace: "repo-my-api-project"

# Hooks (pre/post operations)
hooks:
  pre-commit:
    - lint
    - type-check
    - test-unit
  pre-push:
    - test-integration
  post-merge:
    - deploy-preview  # If on staging branch

# GitHub integration
github:
  auto_sync: true
  issue_labels:
    research: "research"
    feature: "feature"
    bug: "bug"
  pr_auto_create: true
  ci_cd_integration: true

# Cost tracking
cost:
  track: true
  alerts:
    threshold: 80%  # Alert when repo hits 80% of global budget allocation

# Secrets (references to centralized vault)
secrets:
  - name: DATABASE_URL
    vault_key: repo-my-api-project/database-password
  - name: API_KEY
    vault_key: repo-my-api-project/api-secret
```

#### DevContainer Configuration

**Location**: `.devcontainer/devcontainer.json`

**Auto-generated** based on detected stack:

```json
{
  "name": "my-api-project",
  "image": "mcr.microsoft.com/devcontainers/typescript-node:18",

  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },

  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-vscode.vscode-typescript-next"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
          "source.fixAll.eslint": true
        }
      }
    }
  },

  "forwardPorts": [3000, 5432],

  "postCreateCommand": "npm install",

  "remoteUser": "node"
}
```

**Opinionated Artifact Locations**:
```
my-api-project/
├── .agentic-dev/              # All agentic artifacts (auto-created)
│   ├── specs/                 # SPARC specifications
│   ├── pseudocode/            # SPARC pseudocode
│   ├── architecture/          # SPARC architecture docs
│   ├── decisions/             # Architecture Decision Records (ADRs)
│   └── metrics/               # Swarm execution metrics
├── .devcontainer/             # Codespaces/devcontainer config
├── .github/                   # GitHub automation
│   ├── workflows/             # CI/CD pipelines (auto-generated)
│   └── ISSUE_TEMPLATE/        # Issue templates
├── docs/                      # User-facing documentation
├── src/                       # Source code
├── tests/                     # Test files
└── .agentic-dev.yaml          # Repo configuration (minimal)
```

---

### 11. Monitoring & Control via Claude Code MCP

**Component**: claude-flow MCP tools (02-claude-flow.md) - 87 tools

#### Real-Time Monitoring

**Via Claude Code conversational interface**:

```
User: "Show swarm status"

System (MCP call: swarm_status):
┌──────────────────────────────────────────────┐
│ Active Swarms: 2                             │
├──────────────────────────────────────────────┤
│ Swarm ID: swarm-001                          │
│   Repo: my-api-project                       │
│   Task: SPARC Architecture Phase             │
│   Agents: 5 (architecture, system-architect, │
│              backend-dev, coder, reviewer)   │
│   Status: In Progress (45% complete)         │
│   Duration: 12 minutes                       │
│   Topology: Hierarchical                     │
│                                              │
│ Swarm ID: swarm-002                          │
│   Repo: research-repo                        │
│   Task: Research Issue #47                   │
│   Agents: 3 (scout-explorer, researcher,     │
│              analyst)                        │
│   Status: In Progress (78% complete)         │
│   Duration: 34 minutes                       │
│   Topology: Mesh                             │
└──────────────────────────────────────────────┘

User: "Show memory usage"

System (MCP call: memory_usage):
┌──────────────────────────────────────────────┐
│ AgentDB Statistics                           │
├──────────────────────────────────────────────┤
│ Database Size: 247 MB                        │
│ Total Namespaces: 18                         │
│ Query Performance: 2.1ms avg                 │
│                                              │
│ Breakdown by Namespace:                      │
│   central/*: 89 MB (architecture patterns)   │
│   repo-my-api-project/*: 45 MB               │
│   repo-research/*: 67 MB                     │
│   active-swarm-001/*: 12 MB (ephemeral)      │
│   active-swarm-002/*: 8 MB (ephemeral)       │
│   Other: 26 MB                               │
└──────────────────────────────────────────────┘

User: "Show token usage for my-api-project"

System (MCP call: token_usage):
┌──────────────────────────────────────────────┐
│ Token Usage: my-api-project                  │
├──────────────────────────────────────────────┤
│ This Month: 1,247,832 tokens                 │
│ Cost: $14.23                                 │
│                                              │
│ Breakdown:                                   │
│   Input tokens: 892,445 ($8.03)              │
│   Output tokens: 355,387 ($6.20)             │
│                                              │
│ By Task:                                     │
│   SPARC workflows: 745,223 tokens ($8.92)    │
│   Code reviews: 312,445 tokens ($3.12)       │
│   Research: 190,164 tokens ($2.19)           │
│                                              │
│ Optimization:                                │
│   Local execution saved: ~$127.45            │
│   Multi-Model Router savings: 87%            │
└──────────────────────────────────────────────┘

User: "Cancel swarm-001"

System (MCP call: swarm_destroy):
✅ Swarm swarm-001 gracefully terminated.
   • Agents notified and shut down
   • In-progress work saved to repo-my-api-project/experiments/
   • Ephemeral namespace archived
   • Memory persisted to AgentDB
   • Cost: $2.34 (tokens: 187,445)
```

#### Performance Bottleneck Detection

**Proactive monitoring** (auto-triggered every hour):

```typescript
async function detectBottlenecks() {
  const metrics = await collectMetrics();

  // Check for slow queries
  if (metrics.agentdb.avg_query_latency > 10) {
    alert('AgentDB query latency degraded: ${metrics.agentdb.avg_query_latency}ms');
  }

  // Check for memory pressure
  if (metrics.system.memory_usage > 90) {
    alert('High memory usage on Pi 5: ${metrics.system.memory_usage}%');
    // Suggestion: Offload swarms to cloud
  }

  // Check for swarm coordination delays
  if (metrics.swarms.coordination_latency > 5000) {
    alert('Swarm coordination slow: Consider switching topology');
  }

  // Check for cost anomalies
  if (metrics.costs.daily_spend > metrics.costs.daily_average * 2) {
    alert('Cost spike detected: ${metrics.costs.daily_spend} (avg: ${metrics.costs.daily_average})');
  }
}
```

---

### 12. Raspberry Pi 5 Optimization Strategy (Docker-Centric)

#### Resource Specifications
- **RAM**: 16GB (4x previous capacity)
- **CPU**: Quad-core ARM Cortex-A76 @ 2.4GHz
- **Storage**: 256GB NVMe SSD (expandable with external drives)
- **Architecture**: ARM64 (Docker multi-arch support)

#### Optimization Strategies (Docker + 16GB RAM)

**1. Container-Based Resource Management**
```yaml
# With 16GB RAM, can run MORE locally before cloud offload:

Docker Resource Limits:
├── orchestrator: 4GB RAM, 2 CPU cores
│   • Can handle 5-8 parallel swarms
│   • 64+ agents available
│   • Dynamic topology switching
│
├── agentdb: 2GB RAM, 1 CPU core
│   • 256GB storage volume
│   • 2-3ms query latency maintained
│   • Namespace isolation enforced
│
├── github-sync: 1GB RAM, 1 CPU core
│   • 10-15 repos cloned locally
│   • 5-minute sync interval
│
├── monitoring: 1GB RAM, 0.5 CPU cores
│   • Real-time metrics
│   • 30-day retention
│
└── secret-manager: 512MB RAM, 0.5 CPU cores
    • Encrypted vault access
    • Audit trail logging

Tasks to run on Pi 5 (16GB capacity):
✅ 5-8 parallel swarms (vs 2-3 with 8GB)
✅ Complex SPARC workflows (up to 2 hours)
✅ Multi-repo operations (3-4 repos simultaneously)
✅ Large code generation (within memory limits)
✅ Research with moderate scraping
✅ All AgentDB operations (local SQLite)
✅ GitHub sync for 10-15 repos

Tasks to offload to cloud (Kubernetes):
☁️ 10+ parallel swarms
☁️ Heavy ML training (ruv-FANN)
☁️ Massive parallel research (50+ sources)
☁️ Long-running tasks (>3 hours)
☁️ High-throughput batch processing
```

**2. Kubernetes Cloud Migration (When Scale Needed)**

**When to migrate to cloud (from Pi 5)**:
```typescript
function shouldMigrateToCloud(metrics: SystemMetrics): boolean {
  // Consistent high memory usage (16GB Pi 5 limit)
  if (metrics.avgMemoryUsage7d > 85%) return true;

  // Frequent parallel swarms (>8 simultaneously)
  if (metrics.avgActiveSwarms > 8) return true;

  // Long-running workflows regularly exceed Pi 5 capacity
  if (metrics.avgWorkflowDuration > 3 * 60 * 60) return true; // > 3 hours

  // Multi-repo operations becoming frequent (>5 repos at once)
  if (metrics.avgReposActive > 5) return true;

  // Cost of cloud compute < cost of upgrading Pi infrastructure
  if (metrics.cloudCostSavings > 0) return true;

  // Team growth (multiple developers using service)
  if (metrics.concurrentUsers > 3) return true;

  return false;
}
```

**Cloud migration path** (Docker → Kubernetes):
```bash
# Step 1: Push Docker images to registry
docker tag agentic-dev/orchestrator:latest gcr.io/project/orchestrator:v1
docker push gcr.io/project/orchestrator:v1

# Step 2: Convert docker-compose.yml to Kubernetes manifests
kompose convert -f docker-compose.yml -o k8s/

# Step 3: Deploy to Kubernetes (GKE, EKS, AKS)
kubectl apply -f k8s/

# Step 4: Horizontal scaling (10+ orchestrator pods)
kubectl scale deployment orchestrator --replicas=10
```

**Cloud deployment options**:
- **Kubernetes (Recommended)**: AWS EKS, GCP GKE, Azure AKS
  - Horizontal scaling (10+ orchestrator replicas)
  - Same Docker images from Pi 5
  - Persistent volumes for AgentDB
  - Load balancer for MCP traffic
- **Docker Swarm**: Lighter alternative to K8s
- **Managed containers**: AWS ECS, GCP Cloud Run, Azure Container Instances

**3. Docker Volume Management (256GB Storage)**

**AgentDB Docker volume optimization**:
```bash
# Docker volume mounted to /mnt/storage/agentdb-data (256GB)
# Scheduled cleanup via Docker container cron job

# Cleanup container (runs daily at 2 AM)
docker exec agentdb node /app/scripts/cleanup.js
```

```sql
-- Periodic cleanup (runs daily at 2 AM in agentdb container)
DELETE FROM memories
WHERE namespace LIKE 'active-swarm-%'
  AND created_at < NOW() - INTERVAL '24 hours';

DELETE FROM memories
WHERE namespace LIKE 'repo-%/experiments/%'
  AND created_at < NOW() - INTERVAL '30 days';

-- Vacuum to reclaim space (SQLite optimization)
VACUUM;
```

**Namespace size limits (16GB RAM, 256GB storage)**:
```typescript
// With 256GB storage, more generous limits
const NAMESPACE_LIMITS = {
  'central/*': 10 * 1024 * 1024 * 1024,  // 10 GB max (architecture patterns)
  'repo-*/architecture/*': 2 * 1024 * 1024 * 1024,  // 2 GB per repo
  'repo-*/experiments/*': 500 * 1024 * 1024,  // 500 MB per repo (30-day TTL)
  'active-swarm-*/*': 200 * 1024 * 1024,  // 200 MB per swarm (ephemeral)
  'research/*': 1 * 1024 * 1024 * 1024,  // 1 GB per research issue (90-day TTL)
};

// Total maximum: ~50GB for AgentDB, 200GB for repos, rest for system
```

**Docker volume expansion** (if 256GB fills up):
```bash
# External drive mounting (USB 3.0 or NAS)
sudo mkdir -p /mnt/external-storage
sudo mount /dev/sda1 /mnt/external-storage

# Update docker-compose.yml volume binding
volumes:
  agentdb-data:
    driver: local
    driver_opts:
      device: /mnt/external-storage/agentdb-data
```

**4. Docker Storage Layout (256GB NVMe)**

**Recommended setup**:
- **256GB NVMe SSD**: Primary storage for Docker volumes
- **External HDD/NAS** (optional): Expandable storage for archives
- **Boot**: microSD or eMMC (32GB minimum for Raspberry Pi OS)

**Docker volume file structure**:
```
/mnt/storage/                   # 256GB NVMe SSD (mounted)
├── agentdb-data/               # Docker volume: agentdb-data
│   └── agentdb.db             # SQLite database (up to 50GB)
│
├── repos/                      # Docker volume: repos-data
│   ├── repo-A/                # Git clone
│   ├── repo-B/                # Git clone
│   ├── repo-C/                # Git clone
│   └── research-repo/         # Research findings
│
├── secrets/                    # Docker volume: secrets-vault
│   └── vault.db               # Encrypted secrets (AES-256-GCM)
│
├── agents/                     # Docker volume: agent-definitions
│   ├── core/                  # Core agent .md files
│   ├── sparc/                 # SPARC agent definitions
│   ├── research/              # Research agents
│   └── ...                    # 64+ total agents
│
├── metrics/                    # Docker volume: metrics-data
│   ├── prometheus/            # Time-series metrics
│   └── analytics/             # Cost tracking
│
└── logs/                       # Docker volume: *-logs
    ├── orchestrator/
    ├── github-sync/
    └── monitoring/

/home/pi/agentic-dev/          # Docker Compose project directory
├── docker-compose.yml         # Main orchestration file
├── services/                  # Dockerfiles for each service
│   ├── orchestrator/
│   │   ├── Dockerfile
│   │   └── src/
│   ├── agentdb/
│   │   ├── Dockerfile
│   │   └── src/
│   ├── secret-manager/
│   ├── github-sync/
│   └── monitoring/
│
├── k8s/                       # Kubernetes manifests (for cloud migration)
│   ├── orchestrator.yaml
│   ├── agentdb.yaml
│   └── ...
│
└── scripts/
    ├── start.sh               # docker-compose up -d
    ├── stop.sh                # docker-compose down
    ├── backup.sh              # Volume backups
    └── migrate-to-k8s.sh      # Cloud migration script
```

---

## Implementation Roadmap (Docker-Centric)

### Phase 1: Docker Foundation (Weeks 1-2)

**Goal**: Docker-based infrastructure running on Pi 5 (16GB RAM, 256GB storage)

#### Week 1: Docker & Base Services
- [ ] Install Raspberry Pi OS (64-bit) on Pi 5
- [ ] Install Docker & Docker Compose
  ```bash
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo usermod -aG docker pi
  sudo apt-get install docker-compose
  ```
- [ ] Mount 256GB NVMe SSD to `/mnt/storage`
- [ ] Create Docker volume directories
- [ ] Create project structure: `/home/pi/agentic-dev/`
- [ ] Build base Dockerfiles (orchestrator, agentdb, secret-manager, github-sync, monitoring)
- [ ] Test: `docker-compose up -d` - all containers start successfully

#### Week 2: Service Integration & Testing
- [ ] Configure orchestrator container
  - [ ] Install claude-flow (`npm install claude-flow@alpha`)
  - [ ] Copy 64+ agent definitions to volume
  - [ ] Expose MCP server on port 3000
- [ ] Configure AgentDB container
  - [ ] SQLite database initialization
  - [ ] Namespace isolation setup
  - [ ] TTL cleanup cron job
- [ ] Configure secret-manager container
  - [ ] AES-256-GCM encryption
  - [ ] Vault database creation
  - [ ] API endpoint testing
- [ ] Configure github-sync container
  - [ ] GitHub personal access token (via secret-manager)
  - [ ] Repository discovery
  - [ ] 5-minute sync interval
- [ ] Test:
  - [ ] All containers communicate via Docker network
  - [ ] Sync 3 repositories to Docker volume
  - [ ] Store/retrieve secrets from vault

**Deliverables**:
- [ ] Docker Compose environment running on Pi 5
- [ ] All 5 containers operational
- [ ] 3 repos synced in Docker volume
- [ ] Secret vault operational

---

### Phase 2: Memory & Namespace (Weeks 3-4)

**Goal**: AgentDB with proper isolation and TTL in Docker container

#### Week 3: Namespace Architecture (AgentDB Container)
- [ ] Update AgentDB container with namespace schema
  - [ ] `central/*` (indefinite, 10GB max)
  - [ ] `repo-{name}/*` (hybrid TTL, 2GB per repo)
  - [ ] `active-swarm-{id}/*` (ephemeral, 200MB max)
  - [ ] `research/*` (90-day TTL, 1GB per issue)
- [ ] Implement namespace ACLs in AgentDB service
  - [ ] API: Swarm can only access authorized namespaces
  - [ ] Cross-namespace queries require permission token
- [ ] Add TTL cleanup job to AgentDB container
  - [ ] Docker cron: daily cleanup at 2 AM
  - [ ] SQLite VACUUM weekly
  - [ ] Expose cleanup API endpoint
- [ ] Docker volume: Ensure 50GB allocated for AgentDB data

#### Week 4: Pattern Suggestion System (Orchestrator Container)
- [ ] Implement cross-namespace semantic search in orchestrator
  - [ ] Query AgentDB API: `http://agentdb:3001/search`
  - [ ] Aggregate results from multiple namespaces
- [ ] Build pattern suggestion logic
  - [ ] Trigger: new feature request (webhook)
  - [ ] Search: `central/*` and other `repo-*/architecture/*`
  - [ ] Score: confidence ranking (0-1)
  - [ ] Return top 5 suggestions
- [ ] Test: Suggest pattern from Repo A when building in Repo B
  - [ ] Verify Docker network communication
  - [ ] Check namespace isolation (no leakage)

**Deliverables**:
- [ ] Namespace isolation working in AgentDB container
- [ ] TTL cleanup automated via Docker cron
- [ ] Pattern suggestions functional via container API

---

### Phase 3: Development Workflow (Weeks 5-7)

**Goal**: SPARC → TDD → Truth Verification pipeline

#### Week 5: SPARC Integration
- [ ] Configure SPARC skills (specification, pseudocode, architecture)
- [ ] Create `.agentic-dev/` directory structure template
- [ ] Test: Run SPARC workflow on sample feature
  - [ ] Specification phase → `.agentic-dev/specs/`
  - [ ] Pseudocode phase → `.agentic-dev/pseudocode/`
  - [ ] Architecture phase → `.agentic-dev/architecture/`

#### Week 6: TDD London School
- [ ] Integrate tdd-london-swarm skill
- [ ] Configure test frameworks (Jest, pytest, etc. based on stack)
- [ ] Test: Build simple API endpoint with TDD
  - [ ] Write failing test first
  - [ ] Implement minimal code
  - [ ] Refactor and iterate

#### Week 7: Truth Verification
- [ ] Configure truth-verification skill
- [ ] Set threshold: 0.95 (95% accuracy required)
- [ ] Implement auto-rollback on failure
- [ ] Test: Submit intentionally flawed code, verify rollback
- [ ] Test: Submit valid code, verify approval

**Deliverables**:
- [ ] End-to-end SPARC → TDD → Truth Verification working
- [ ] Sample feature built and validated
- [ ] Artifacts stored in `.agentic-dev/`

---

### Phase 4: Research Mode (Weeks 8-9)

**Goal**: Read-only research swarms with GOAP + FACT

#### Week 8: Research Workflow
- [ ] Configure research-only access mode
  - [ ] Read-only permissions for code repos
  - [ ] Write access to `research-repo/issues/{N}/`
- [ ] Integrate GOAP system for research planning
- [ ] Integrate FACT for tool-based retrieval
- [ ] Test: Spawn research swarm on sample issue
  - [ ] Multi-agent: scout-explorer + researcher + analyst
  - [ ] Output: Markdown with citations

#### Week 9: GitHub Issue Integration
- [ ] Implement issue event handler
  - [ ] Label detection (`research`, `feature`, `bug`)
  - [ ] Auto-spawn appropriate swarm
- [ ] Link research findings to development issues
- [ ] Test: Create research issue → auto-swarm → findings → link to dev issue

**Deliverables**:
- [ ] Research mode operational
- [ ] GitHub issue automation working
- [ ] Research-to-development pipeline established

---

### Phase 5: Cross-Repo & Monitoring (Weeks 10-11)

**Goal**: Multi-repo operations and real-time monitoring

#### Week 10: Cross-Repo Capabilities
- [ ] Implement module referencing system
  - [ ] Cross-namespace search for similar patterns
  - [ ] Read-only access to other repos for analysis
  - [ ] Recommendation engine (reuse vs replicate)
- [ ] Test: Build feature in Repo B referencing Repo A module

#### Week 11: Monitoring & Control
- [ ] Expose MCP tools for monitoring
  - [ ] `swarm_status` - Real-time swarm activity
  - [ ] `memory_usage` - AgentDB statistics
  - [ ] `token_usage` - Cost tracking per repo
- [ ] Implement swarm control
  - [ ] `swarm_destroy` - Cancel active swarm
  - [ ] Priority override
- [ ] Build performance bottleneck detection
  - [ ] Auto-alert on anomalies
  - [ ] Suggestions for optimization

**Deliverables**:
- [ ] Cross-repo referencing working
- [ ] Real-time monitoring via Claude Code
- [ ] Swarm control operational

---

### Phase 6: CI/CD & Optimization (Weeks 12-13)

**Goal**: GitHub Actions integration and Pi 5 optimization

#### Week 12: CI/CD Integration
- [ ] Auto-generate GitHub Actions workflows
  - [ ] Based on detected stack
  - [ ] Standard: lint, test, build, deploy
- [ ] Implement hooks system
  - [ ] pre-commit, pre-push, post-merge
  - [ ] Integration with local git hooks
- [ ] Configure PR automation
  - [ ] Auto-create PRs after SPARC completion
  - [ ] Request code-review-swarm
  - [ ] Auto-label based on changes

#### Week 13: Pi 5 Optimization
- [ ] Implement hybrid cloud offload
  - [ ] Detect resource pressure
  - [ ] Offload heavy swarms to cloud workers
- [ ] Optimize AgentDB performance
  - [ ] Index tuning
  - [ ] Query optimization
  - [ ] Memory cleanup automation
- [ ] Performance testing
  - [ ] Load test: 3 active swarms simultaneously
  - [ ] Measure: latency, memory, cost

**Deliverables**:
- [ ] CI/CD pipelines auto-generated
- [ ] Hybrid cloud offload working
- [ ] System optimized for Pi 5 constraints

---

### Phase 7: Polish & Production (Week 14)

**Goal**: Production-ready Docker service with cloud migration path

#### Tasks
- [ ] Security hardening
  - [ ] Post-quantum crypto enabled (QuDAG) in secret-manager container
  - [ ] Zero-trust enforcement via Docker network policies
  - [ ] Secret vault audit logging
  - [ ] Container image scanning (Trivy, Snyk)
- [ ] Documentation
  - [ ] Docker Compose setup guide
  - [ ] Kubernetes migration guide
  - [ ] MCP tool reference
  - [ ] Troubleshooting guide (container logs, debugging)
- [ ] Backup & recovery (Docker volumes)
  - [ ] Daily backup script: `docker run --rm -v agentdb-data:/data -v /backup:/backup alpine tar czf /backup/agentdb-$(date +%Y%m%d).tar.gz /data`
  - [ ] Secret vault backup (encrypted)
  - [ ] Disaster recovery plan (restore from volume backups)
- [ ] Testing
  - [ ] End-to-end workflow testing (Docker environment)
  - [ ] Multi-repo scenario testing
  - [ ] Container failure mode testing (restart policies)
  - [ ] Load testing (5-8 parallel swarms on 16GB Pi 5)
- [ ] Kubernetes preparation
  - [ ] Push Docker images to container registry (Docker Hub, GCR, ECR)
  - [ ] Generate Kubernetes manifests: `kompose convert`
  - [ ] Test K8s deployment locally (minikube or k3s on Pi 5)

**Deliverables**:
- [ ] Production-ready Docker Compose service
- [ ] Comprehensive documentation (Docker + K8s)
- [ ] Backup & recovery automated (Docker volumes)
- [ ] Kubernetes migration path ready

---

## Technical Specifications

### System Requirements (Docker-Centric)

**Raspberry Pi 5**:
- **Model**: 16GB RAM (confirmed available)
- **Storage**: 256GB NVMe SSD (primary), expandable with external drives
- **Network**: Ethernet preferred (WiFi acceptable)
- **Power**: Official 27W USB-C power supply
- **OS**: Raspberry Pi OS 64-bit (Debian-based, Docker-compatible)
- **Architecture**: ARM64 (for Docker multi-arch images)

**Software Stack (Docker-Based)**:
```yaml
Host System (Pi 5):
  - OS: Raspberry Pi OS 64-bit (Bookworm or later)
  - Docker: 24.0+ (with BuildKit support)
  - Docker Compose: 2.20+
  - Git: 2.40+ (for docker build context)

Docker Images (Built for ARM64):
  orchestrator:
    - Base: node:18-alpine
    - Runtime: Node.js 18+
    - Dependencies: claude-flow v2.7.0+, 87 MCP tools
    - Size: ~300MB (optimized Alpine)

  agentdb:
    - Base: node:18-alpine
    - Runtime: Node.js 18+ with better-sqlite3
    - Database: SQLite 3.40+
    - Size: ~150MB

  secret-manager:
    - Base: node:18-alpine
    - Runtime: Node.js 18+
    - Crypto: AES-256-GCM, QuDAG (post-quantum)
    - Size: ~100MB

  github-sync:
    - Base: node:18-alpine
    - Runtime: Node.js 18+
    - Git: 2.40+ (for cloning/syncing)
    - Size: ~200MB

  monitoring:
    - Base: prom/prometheus:latest (ARM64)
    - Runtime: Prometheus + custom Node.js API
    - Size: ~250MB

Total Docker Image Storage: ~1GB
Docker Volume Data: ~50GB (AgentDB) + 200GB (repos) = 250GB

Cloud Migration (Kubernetes):
  - Container Registry: Docker Hub, GCR, ECR, ACR
  - K8s Version: 1.28+ (EKS, GKE, AKS)
  - Persistent Volumes: 100GB per node (for AgentDB replica)
  - Ingress: NGINX or cloud load balancer
  - Autoscaling: HPA (Horizontal Pod Autoscaler) for orchestrator
```

### Network Architecture

```
Internet
    │
    ├─> GitHub API (HTTPS)
    │   • Repository sync
    │   • Issue/PR management
    │   • Actions webhooks
    │
    ├─> Anthropic API (HTTPS)
    │   • Claude Sonnet 4
    │   • For complex reasoning
    │
    ├─> OpenRouter API (HTTPS, optional)
    │   • Multi-model routing
    │   • Cost optimization
    │
    └─> Cloud Workers (QUIC, optional)
        • Flow Nexus platform
        • Or generic VMs

Pi 5 (Local Network)
    │
    └─> Claude Code (MCP via stdio)
        • Conversational interface
        • Real-time monitoring
```

**No inbound connections required** - All outbound HTTPS/QUIC

---

## File Structure (Docker-Centric)

```
/mnt/storage/                        # 256GB NVMe SSD (Docker volumes)
├── agentdb-data/                    # Docker volume: agentdb-data
│   └── agentdb.db                  # SQLite (up to 50GB)
│
├── repos/                           # Docker volume: repos-data
│   ├── repo-A/
│   │   ├── .agentic-dev.yaml       # Repo config
│   │   ├── .agentic-dev/           # Artifacts (SPARC outputs)
│   │   │   ├── specs/
│   │   │   ├── pseudocode/
│   │   │   ├── architecture/
│   │   │   ├── decisions/
│   │   │   └── metrics/
│   │   └── .devcontainer/
│   ├── repo-B/
│   ├── repo-C/
│   └── research-repo/
│       └── issues/
│           ├── 1/findings.md
│           ├── 2/findings.md
│           └── ...
│
├── secrets/                         # Docker volume: secrets-vault
│   └── vault.db                    # Encrypted (AES-256-GCM)
│
├── agents/                          # Docker volume: agent-definitions
│   ├── core/
│   ├── sparc/
│   ├── research/
│   ├── github/
│   └── ...                         # 64+ agent .md files
│
├── metrics/                         # Docker volume: metrics-data
│   ├── prometheus/
│   └── analytics/
│
└── backups/                         # Daily Docker volume backups
    ├── agentdb-20251021.tar.gz
    └── secrets-20251021.tar.gz.enc

/home/pi/agentic-dev/                # Docker Compose project
├── docker-compose.yml              # Main orchestration
├── .env                            # Environment variables (secrets)
│
├── services/                        # Container source code
│   ├── orchestrator/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── src/
│   │       ├── index.ts
│   │       ├── mcp-server.ts
│   │       └── swarm-coordinator.ts
│   │
│   ├── agentdb/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── src/
│   │       ├── index.ts
│   │       ├── sqlite-manager.ts
│   │       ├── namespace-acl.ts
│   │       └── scripts/cleanup.js
│   │
│   ├── secret-manager/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── src/
│   │       ├── index.ts
│   │       ├── vault-api.ts
│   │       └── encryption.ts
│   │
│   ├── github-sync/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── src/
│   │       ├── index.ts
│   │       ├── sync-engine.ts
│   │       └── webhook-handler.ts
│   │
│   └── monitoring/
│       ├── Dockerfile
│       ├── prometheus.yml
│       └── src/
│           ├── index.ts
│           └── metrics-collector.ts
│
├── k8s/                            # Kubernetes manifests (cloud migration)
│   ├── namespace.yaml
│   ├── orchestrator-deployment.yaml
│   ├── orchestrator-service.yaml
│   ├── agentdb-statefulset.yaml
│   ├── agentdb-pvc.yaml
│   ├── secret-manager-deployment.yaml
│   ├── github-sync-deployment.yaml
│   ├── monitoring-deployment.yaml
│   └── ingress.yaml
│
└── scripts/
    ├── start.sh                    # docker-compose up -d
    ├── stop.sh                     # docker-compose down
    ├── restart.sh                  # Restart specific service
    ├── backup.sh                   # Backup Docker volumes
    ├── restore.sh                  # Restore from backups
    ├── logs.sh                     # docker-compose logs -f
    ├── build.sh                    # Rebuild all images
    ├── push-images.sh              # Push to container registry
    └── migrate-to-k8s.sh           # Convert + deploy to K8s
```

---

## Cost Estimates

### Monthly Operating Costs (Docker-Based, Pi 5 16GB)

**Infrastructure (One-time)**:
- Raspberry Pi 5 (16GB): $120-150
- 256GB NVMe SSD: $30-40
- Cooling (heatsink/fan): $10-15
- **Total one-time**: ~$160-205

**Infrastructure (Recurring)**:
- Power consumption: ~10W average (Docker containers)
  - Monthly: ~7.3 kWh × $0.12/kWh = **$0.88/month**
- Internet bandwidth: Negligible (GitHub sync, API calls)

**API Costs** (assuming 2-3 active projects, 16GB RAM allows more local execution):

- **Scenario 1: Local-heavy (90% local, 10% API)** ← **16GB enables this**
  - Claude API: ~250K tokens/month = **~$3/month**
  - GitHub API: Free (within limits)
  - Docker overhead: Minimal
  - **Total: ~$4/month** (vs $7/month with 8GB)

- **Scenario 2: Hybrid (70% local, 30% API)**
  - Claude API: ~1M tokens/month = **~$12/month**
  - Cloud workers (optional): **~$5/month** (minimal offload needed)
  - **Total: ~$17/month** (vs $34/month with 8GB)

- **Scenario 3: Heavy usage (50% local, 50% API)**
  - Claude API: ~3M tokens/month = **~$36/month**
  - Cloud workers: **~$15/month** (moderate offload)
  - **Total: ~$51/month** (vs $90/month with 8GB)

**With Multi-Model Router optimization**: 85-99% savings
- Scenario 3 → **~$5-8/month** (massive savings!)

**Cloud Migration Costs** (if scaling beyond Pi 5):
- **Kubernetes (AWS EKS, GCP GKE, Azure AKS)**:
  - Control plane: $75/month (managed K8s)
  - 3x worker nodes (4GB RAM each): ~$100/month
  - Persistent volumes: ~$10/month (100GB)
  - Load balancer: ~$20/month
  - **Total cloud**: ~$205/month (10+ parallel swarms, enterprise scale)

**Cost Comparison**:
```
Pi 5 (16GB) Local:           $4-51/month (2-3 projects)
Pi 5 + Cloud hybrid:         $20-80/month (5-8 projects)
Full Cloud (Kubernetes):     $205+/month (10+ projects, team scale)
```

---

## Kubernetes Migration Guide (Cloud Scaling)

### When to Migrate from Pi 5 to Kubernetes

**Triggers** (automated monitoring can detect these):
- Consistent >85% memory usage on Pi 5 over 7 days
- Regularly running 8+ parallel swarms
- Multi-repo operations exceeding Pi 5 capacity (5+ repos simultaneously)
- Team growth (3+ developers needing concurrent access)
- Need for high availability (99.9% uptime SLA)

### Migration Steps (Docker → Kubernetes)

#### Step 1: Prepare Docker Images

```bash
# Tag images for container registry
docker tag agentic-dev/orchestrator:latest gcr.io/my-project/orchestrator:v1.0.0
docker tag agentic-dev/agentdb:latest gcr.io/my-project/agentdb:v1.0.0
docker tag agentic-dev/secret-manager:latest gcr.io/my-project/secret-manager:v1.0.0
docker tag agentic-dev/github-sync:latest gcr.io/my-project/github-sync:v1.0.0
docker tag agentic-dev/monitoring:latest gcr.io/my-project/monitoring:v1.0.0

# Push to registry (GCR, ECR, ACR, or Docker Hub)
docker push gcr.io/my-project/orchestrator:v1.0.0
docker push gcr.io/my-project/agentdb:v1.0.0
# ... etc for all images
```

#### Step 2: Convert Docker Compose to Kubernetes

```bash
# Install kompose (conversion tool)
curl -L https://github.com/kubernetes/kompose/releases/download/v1.30.0/kompose-linux-arm64 -o kompose
chmod +x kompose
sudo mv kompose /usr/local/bin/

# Convert docker-compose.yml to Kubernetes manifests
cd /home/pi/agentic-dev
kompose convert -f docker-compose.yml -o k8s/

# This generates: deployments, services, persistentvolumeclaims, configmaps
```

#### Step 3: Customize Kubernetes Manifests

**Example: Orchestrator Deployment** (`k8s/orchestrator-deployment.yaml`):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orchestrator
  labels:
    app: agentic-dev
    component: orchestrator
spec:
  replicas: 3  # Start with 3 replicas for HA
  selector:
    matchLabels:
      app: agentic-dev
      component: orchestrator
  template:
    metadata:
      labels:
        app: agentic-dev
        component: orchestrator
    spec:
      containers:
      - name: orchestrator
        image: gcr.io/my-project/orchestrator:v1.0.0
        ports:
        - containerPort: 3000
          name: mcp-server
        env:
        - name: NODE_ENV
          value: "production"
        - name: AGENTDB_URL
          value: "http://agentdb:3001"
        - name: SECRET_MANAGER_URL
          value: "http://secret-manager:3002"
        - name: GITHUB_SYNC_URL
          value: "http://github-sync:3003"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        volumeMounts:
        - name: agent-definitions
          mountPath: /app/agents
          readOnly: true
        - name: logs
          mountPath: /app/logs
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
      volumes:
      - name: agent-definitions
        persistentVolumeClaim:
          claimName: agent-definitions-pvc
      - name: logs
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: orchestrator
  labels:
    app: agentic-dev
    component: orchestrator
spec:
  type: LoadBalancer
  ports:
  - port: 3000
    targetPort: 3000
    name: mcp-server
  selector:
    app: agentic-dev
    component: orchestrator
```

**Example: AgentDB StatefulSet** (`k8s/agentdb-statefulset.yaml`):

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: agentdb
  labels:
    app: agentic-dev
    component: agentdb
spec:
  serviceName: agentdb
  replicas: 1  # Single replica for SQLite (or use PostgreSQL for multi-replica)
  selector:
    matchLabels:
      app: agentic-dev
      component: agentdb
  template:
    metadata:
      labels:
        app: agentic-dev
        component: agentdb
    spec:
      containers:
      - name: agentdb
        image: gcr.io/my-project/agentdb:v1.0.0
        ports:
        - containerPort: 3001
          name: api
        env:
        - name: SQLITE_PATH
          value: "/data/agentdb.db"
        - name: NAMESPACE_ISOLATION
          value: "enabled"
        - name: TTL_CLEANUP_ENABLED
          value: "true"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        volumeMounts:
        - name: agentdb-data
          mountPath: /data
        livenessProbe:
          httpGet:
            path: /health
            port: 3001
          initialDelaySeconds: 15
          periodSeconds: 10
      volumes:
      - name: agentdb-data
        persistentVolumeClaim:
          claimName: agentdb-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: agentdb
  labels:
    app: agentic-dev
    component: agentdb
spec:
  clusterIP: None  # Headless service for StatefulSet
  ports:
  - port: 3001
    targetPort: 3001
    name: api
  selector:
    app: agentic-dev
    component: agentdb
```

**Example: Persistent Volume Claim** (`k8s/agentdb-pvc.yaml`):

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: agentdb-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi  # Cloud storage for AgentDB
  storageClassName: standard  # or premium-rwo for faster SSD
```

#### Step 4: Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace agentic-dev

# Apply all manifests
kubectl apply -f k8s/ -n agentic-dev

# Verify deployment
kubectl get pods -n agentic-dev
kubectl get services -n agentic-dev
kubectl get pvc -n agentic-dev

# Check logs
kubectl logs -f deployment/orchestrator -n agentic-dev
kubectl logs -f statefulset/agentdb -n agentic-dev
```

#### Step 5: Configure Autoscaling (HPA)

```yaml
# k8s/orchestrator-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: orchestrator-hpa
  namespace: agentic-dev
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: orchestrator
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

```bash
kubectl apply -f k8s/orchestrator-hpa.yaml -n agentic-dev
```

#### Step 6: Data Migration (Pi 5 → Cloud)

```bash
# 1. Backup AgentDB from Pi 5
docker exec agentdb sqlite3 /data/agentdb.db ".backup /data/backup.db"
docker cp agentdb:/data/backup.db ./agentdb-backup.db

# 2. Upload to cloud storage
gsutil cp agentdb-backup.db gs://my-bucket/migration/

# 3. Restore in Kubernetes pod
kubectl cp agentdb-backup.db agentdb-0:/data/agentdb.db -n agentic-dev

# 4. Verify data integrity
kubectl exec -it agentdb-0 -n agentic-dev -- sqlite3 /data/agentdb.db "SELECT COUNT(*) FROM memories;"
```

### Kubernetes vs Docker Compose Comparison

| Feature | Pi 5 (Docker Compose) | Kubernetes (Cloud) |
|---------|----------------------|-------------------|
| **Scalability** | 5-8 parallel swarms | 10-100+ parallel swarms |
| **High Availability** | Single node (99% uptime) | Multi-node (99.9% uptime) |
| **Orchestrator replicas** | 1 | 3-10 (auto-scaled) |
| **AgentDB** | Single SQLite instance | StatefulSet with backups |
| **Cost** | $4-51/month | $205+/month |
| **Management** | Manual (docker-compose) | Automated (K8s controllers) |
| **Deployment** | `docker-compose up` | `kubectl apply` |
| **Monitoring** | Basic Prometheus | Full observability stack |
| **Backup** | Manual scripts | Automated snapshots (Velero) |
| **Networking** | Docker bridge | Service mesh (Istio, optional) |

### Cloud Provider Options

**AWS EKS** (Elastic Kubernetes Service):
```bash
# Create EKS cluster
eksctl create cluster --name agentic-dev --region us-west-2 --nodes 3 --node-type t3.medium

# Deploy
kubectl apply -f k8s/ -n agentic-dev
```

**GCP GKE** (Google Kubernetes Engine):
```bash
# Create GKE cluster
gcloud container clusters create agentic-dev --zone us-central1-a --num-nodes 3 --machine-type n1-standard-2

# Deploy
kubectl apply -f k8s/ -n agentic-dev
```

**Azure AKS** (Azure Kubernetes Service):
```bash
# Create AKS cluster
az aks create --resource-group agentic-dev-rg --name agentic-dev --node-count 3 --node-vm-size Standard_D2s_v3

# Deploy
kubectl apply -f k8s/ -n agentic-dev
```

### Rollback Strategy (Cloud → Pi 5)

If cloud costs become prohibitive or scaling needs decrease:

```bash
# 1. Backup data from Kubernetes
kubectl exec -it agentdb-0 -n agentic-dev -- sqlite3 /data/agentdb.db ".backup /tmp/backup.db"
kubectl cp agentic-dev/agentdb-0:/tmp/backup.db ./cloud-backup.db

# 2. Restore to Pi 5
docker cp cloud-backup.db agentdb:/data/agentdb.db

# 3. Restart Pi 5 Docker Compose
cd /home/pi/agentic-dev
docker-compose down
docker-compose up -d

# 4. Verify
docker exec agentdb sqlite3 /data/agentdb.db "SELECT COUNT(*) FROM memories;"
```

---

## Success Metrics

### Technical KPIs

**Performance**:
- [ ] Swarm spawn time: <30 seconds
- [ ] AgentDB query latency: <5ms (95th percentile)
- [ ] End-to-end SPARC workflow: <3 hours
- [ ] GitHub sync delay: <5 minutes
- [ ] Truth verification: >95% accuracy threshold

**Reliability**:
- [ ] System uptime: >99.5%
- [ ] Swarm completion rate: >90%
- [ ] Memory consistency: 100% (no cross-contamination)
- [ ] Secret vault security: 0 breaches

**Efficiency**:
- [ ] Cost per feature: <$5 (with optimization)
- [ ] Local execution: >70% of tasks
- [ ] Token usage reduction: >30% (vs naive Claude usage)
- [ ] Developer time savings: >50% (vs manual development)

### Business KPIs

**Productivity**:
- [ ] Features shipped per month: +100%
- [ ] Code quality (SWE-Bench equivalent): >80%
- [ ] Research-to-development cycle time: <7 days
- [ ] Cross-repo pattern reuse: >40%

**Developer Experience**:
- [ ] Setup time: <1 hour (new repo onboarding)
- [ ] Context switching time: <2 minutes (between repos)
- [ ] Debugging time: -40% (with swarm assistance)
- [ ] Documentation coverage: 100% (auto-generated)

---

## Next Steps

### Immediate Actions (This Week)

1. **Order hardware** (if not already owned):
   - Raspberry Pi 5 (8GB)
   - NVMe SSD (256GB+)
   - Official power supply

2. **Set up development environment**:
   - Install Raspberry Pi OS
   - Install Node.js, claude-flow
   - Configure MCP server

3. **Create GitHub token**:
   - Personal access token with repo permissions
   - Test: Fetch repositories

4. **Test basic swarm**:
   - Initialize claude-flow
   - Spawn simple swarm
   - Verify AgentDB functionality

### Week 1 Sprint

- [ ] Complete Phase 1, Week 1 tasks (see roadmap)
- [ ] Document initial setup process
- [ ] Create first `.agentic-dev.yaml` template
- [ ] Test: Sync 1 repository successfully

---

## Appendix: Component Reference

### From Research Notes

**AgentDB** (11-agentdb.md):
- Sub-millisecond vector database
- 20 MCP tools for memory operations
- SQLite + better-sqlite3 backend
- 1024-dim hash-based embeddings
- Namespace isolation built-in

**Claude-Flow** (02-claude-flow.md):
- 64 specialized agents
- 87 MCP tools
- SPARC methodology integration
- Truth Verification System (0.95 threshold)
- Swarm topologies: mesh, hierarchical, star, adaptive
- AgentDB-powered ReasoningBank (150x-12,500x faster)

**GOAP System** (02-claude-flow.md):
- Goal-Oriented Action Planning
- Dynamic replanning
- Constraint satisfaction
- Perfect for research exploration

**FACT** (04-FACT.md):
- Tool-based retrieval (replaces vector search)
- SQL query tool, API tool
- Multi-tier caching
- Hybrid local/cloud execution

**Multi-Model Router** (01-agentic-flow.md):
- 85-99% cost savings
- Route to optimal provider
- Local vs cloud intelligent routing

**QuDAG** (07-qudag.md):
- Post-quantum cryptography (ML-KEM, ML-DSA)
- QUIC protocol (50-70% faster than TCP)
- Byzantine fault tolerance
- .dark domains (optional, for advanced security)

**SAFLA** (06-SAFLA.md):
- 4 memory types (vector, episodic, semantic, working)
- 172,000+ ops/sec
- Meta-cognitive engine
- Optional: For advanced memory architecture

---

**Document Version**: 2.0 (Docker-Centric)
**Last Updated**: 2025-10-21
**Status**: Architecture Specification (Docker + Kubernetes Ready)

---

## Summary of Docker-Centric Updates

### Key Changes from Version 1.0

**Hardware Specifications**:
- ✅ **16GB RAM** (updated from 4-8GB) - Enables 5-8 parallel swarms locally
- ✅ **256GB NVMe storage** (updated from unspecified) - Expandable with external drives

**Architecture Transformation**:
- ✅ **Docker Compose** for local Pi 5 deployment (5 containerized services)
- ✅ **Kubernetes manifests** for cloud migration (AWS EKS, GCP GKE, Azure AKS)
- ✅ **Docker volumes** for persistent data (agentdb-data, repos-data, secrets-vault)
- ✅ **Docker networks** for service isolation (agentic-internal, agentic-external)
- ✅ **Multi-arch support** (ARM64 for Pi 5, AMD64 for cloud)

**Benefits**:
- ✅ **Cloud portability**: Same Docker images run on Pi 5 and Kubernetes
- ✅ **Horizontal scaling**: 3-10 orchestrator replicas in cloud
- ✅ **Better resource management**: Docker memory/CPU limits per container
- ✅ **Easier deployment**: `docker-compose up -d` (Pi 5) or `kubectl apply` (K8s)
- ✅ **Cost efficiency**: Run locally on Pi 5 ($4-51/month), scale to cloud when needed ($205+/month)

**New Sections Added**:
1. Docker Compose Configuration (complete YAML with 5 services)
2. Resource Allocation (16GB RAM distribution)
3. Kubernetes Migration Guide (step-by-step with manifests)
4. Docker Storage Layout (volume structure)
5. Cloud Scaling Path (Docker → K8s)
6. Updated Implementation Roadmap (Docker-focused)
7. Updated Cost Estimates (16GB Pi 5 advantages)

**Maintained Features**:
- ✅ All original capabilities (SPARC → TDD → Truth Verification)
- ✅ Namespace isolation (AgentDB)
- ✅ Cross-repo knowledge transfer
- ✅ GitHub integration
- ✅ Post-quantum security
- ✅ Research mode (GOAP + FACT)

**Next Steps**:
- Review this Docker-centric architecture
- Approve for implementation
- Begin Phase 1, Week 1 (Docker Foundation on Pi 5)
