# Agentic Development Template - Complete Index

**Version**: 4.0 (5-Phase Workflow Template)
**Date**: 2025-10-21

This index provides a complete map of all template files and documentation for the 5-phase creation workflow.

---

## 📁 Directory Structure

```
docs/newopps/
├── AGENTIC-DEV-SERVICE-ARCHITECTURE.md    # Main architecture specification
├── 5-PHASE-WORKFLOW-DETAIL.md             # Detailed workflow guide (400+ lines)
│
└── templates/
    ├── INDEX.md                            # This file
    ├── README.md                           # Template overview & quick start
    ├── DEPLOYMENT-GUIDE.md                 # Deployment for all environments (500+ lines)
    │
    ├── devcontainer.json                   # Codespaces/VS Code configuration
    ├── docker-compose.yml                  # Multi-environment deployment
    ├── Dockerfile                          # Container image definition
    │
    └── .agentic/                           # (Template structure, not files)
        ├── agents/                         # 64+ agent definitions (.md files)
        ├── config/                         # Phase configurations (.yml files)
        ├── scripts/                        # Workflow scripts (.sh files)
        └── workflows/                      # Workflow definitions (.yml files)
```

---

## 📚 Documentation Files

### 1. Main Architecture Specification
**File**: `AGENTIC-DEV-SERVICE-ARCHITECTURE.md`

**What it covers**:
- Executive summary of 5-phase workflow
- Complete system architecture
- Container architecture (single agentic-dev container)
- Repository structure and template organization
- HiveMind coordination patterns
- Phase-by-phase workflow details
- Truth verification integration
- Pattern-driven optimization (optional)

**When to read**: Start here for architectural overview

**Size**: ~1,000 lines

---

### 2. 5-Phase Workflow Detail
**File**: `5-PHASE-WORKFLOW-DETAIL.md`

**What it covers**:
- **Phase 1**: Wild Idea + Deep Research (Scout Explorers, Goalie GOAP)
- **Phase 2**: Formalize Scope/Value + High-Level Architecture (Collective Intelligence)
- **Phase 3**: SPARC Planning (Specification → Pseudocode → Architecture)
- **Phase 4**: Human Approval Checkpoint (Review gate)
- **Phase 5**: London TDD Development (Continuous swarm, Truth verification)
- Worker coordination protocol (30s status updates via AgentDB)
- Truth verification integration (≥0.95 threshold)
- Pattern reuse optimization (optional)
- Post-development human review

**When to read**: After understanding architecture, before implementation

**Size**: ~400 lines

---

### 3. Template README
**File**: `templates/README.md`

**What it covers**:
- Quick start for all environments
- 5-phase flow visualization
- Template structure overview
- Key features summary
- Deployment options comparison
- Workflow examples (OAuth2, REST API)
- Performance metrics
- Configuration overview

**When to read**: First file to read when using the template

**Size**: ~300 lines

---

### 4. Deployment Guide
**File**: `templates/DEPLOYMENT-GUIDE.md`

**What it covers**:
- **GitHub Codespaces**: One-click deployment
- **Raspberry Pi 5**: Docker setup, storage config, auto-start on boot
- **Local Docker**: Quick start for development machines
- **Cloud Deployment**: AWS (ECS/EKS), GCP (Cloud Run/GKE), Azure (ACI/AKS)
- Environment variables reference (required, optional, phase-specific)
- Troubleshooting guide (container issues, MCP, AgentDB, memory, permissions)

**When to read**: When deploying to specific environment

**Size**: ~500 lines

---

## 🐳 Container Configuration Files

### 5. devcontainer.json
**File**: `templates/devcontainer.json`

**What it configures**:
- Docker Compose integration
- VS Code extensions (Claude Code, GitHub PR, Jest, Docker)
- Claude Code MCP servers (claude-flow, goalie, agentdb)
- Terminal environment variables
- Container environment (5-phase config, HiveMind, AgentDB, TDD)
- Persistent volumes (AgentDB, GitHub CLI config)
- Port forwarding (3000, 3001, 8080)
- Lifecycle scripts (postCreateCommand, postStartCommand)

**When to use**: GitHub Codespaces, VS Code Dev Containers

**Format**: JSON

**Size**: ~200 lines

---

### 6. docker-compose.yml
**File**: `templates/docker-compose.yml`

**What it configures**:
- Single `agentic-dev` service
- Environment variables (100+ config options)
  - Phase 1-5 configuration
  - HiveMind coordination
  - AgentDB setup
  - TDD configuration (London School)
  - Truth verification
  - Pattern-driven optimization
  - GitHub integration
  - MCP servers
- Volume mounts (workspace, AgentDB, GitHub CLI, agents, patterns, logs)
- Resource limits (12GB RAM, 3 CPUs for Pi 5)
- Health check
- Networks and persistent volumes

**When to use**: Raspberry Pi 5, Local Docker, Cloud deployment

**Format**: YAML (Docker Compose v3.8)

**Size**: ~400 lines

---

### 7. Dockerfile
**File**: `templates/Dockerfile`

**What it builds**:
- Base: Node.js 20 on Debian
- System dependencies (build tools, Git, GitHub CLI, Docker CLI)
- Global NPM packages (claude-flow, goalie, agentdb, TypeScript, Jest, ESLint)
- Workspace structure (/workspace, /data, /app)
- Agent definitions (64+ .md files)
- Workflow scripts (phase-1.sh through phase-5.sh)
- MCP server setup
- AgentDB initialization
- Health check endpoint
- Startup script

**When to use**: Building container image for any environment

**Format**: Dockerfile

**Size**: ~200 lines

---

## 🎯 How to Use This Template

### Option 1: Use as GitHub Template Repository
```bash
1. Create new repo from template (GitHub UI)
2. Clone your new repo
3. Create .env file: cp .env.example .env
4. Add API keys to .env
5. Run: ./.agentic/scripts/setup.sh
```

### Option 2: Copy Files to Existing Project
```bash
1. Copy .devcontainer/ to your project root
2. Copy .agentic/ to your project root
3. Copy docker-compose.yml and Dockerfile
4. Copy .env.example, rename to .env, add API keys
5. Run: docker-compose up -d
```

### Option 3: GitHub Codespaces (Instant)
```bash
1. Add ANTHROPIC_API_KEY to Codespaces secrets
2. Click "Code" → "Create codespace on main"
3. Wait 2-3 minutes for container build
4. Start: ./.agentic/scripts/phase-1-research.sh "idea"
```

---

## 📖 Reading Order for New Users

**1. Quick Start (5 minutes)**
- `templates/README.md` - Template overview
- `templates/DEPLOYMENT-GUIDE.md` (Quick Start section)

**2. Architectural Understanding (15 minutes)**
- `AGENTIC-DEV-SERVICE-ARCHITECTURE.md` (Executive Summary, Architecture sections)
- `5-PHASE-WORKFLOW-DETAIL.md` (Skim all 5 phases)

**3. Deep Dive Before Implementation (30 minutes)**
- `5-PHASE-WORKFLOW-DETAIL.md` (Read each phase in detail)
- `templates/DEPLOYMENT-GUIDE.md` (Your target environment)

**4. During Implementation (Reference)**
- `templates/devcontainer.json` - For Codespaces customization
- `templates/docker-compose.yml` - For environment variable tuning
- `templates/DEPLOYMENT-GUIDE.md` (Troubleshooting section)

---

## 🔧 Customization Points

### Agent Definitions (`.agentic/agents/`)
**Customize**: Add your own specialized agents
**Format**: Markdown files with agent instructions
**Example**: `.agentic/agents/custom/my-specialist.md`

### Phase Configurations (`.agentic/config/`)
**Customize**: Adjust phase behavior
**Format**: YAML configuration files
**Files**:
- `phase-1-research.yml` - Research tools, timeouts
- `phase-2-formalize.yml` - Iteration limits, templates
- `phase-3-sparc.yml` - SPARC methodology settings
- `phase-4-approval.yml` - Approval workflow config
- `phase-5-tdd.yml` - TDD settings, worker count, thresholds

### Workflow Scripts (`.agentic/scripts/`)
**Customize**: Modify workflow execution
**Format**: Bash scripts
**Files**:
- `setup.sh` - One-time setup (install dependencies, init AgentDB)
- `phase-1-research.sh` - Launch research agents
- `phase-2-formalize.sh` - Launch formalization agents
- `phase-3-sparc.sh` - Launch SPARC planning
- `phase-4-approve.sh` - Human approval workflow
- `phase-5-develop.sh` - Launch TDD swarm

### Environment Variables (`.env`)
**Customize**: Tune behavior for your needs
**See**: `DEPLOYMENT-GUIDE.md` (Environment Variables section)
**Common changes**:
- `MAX_PARALLEL_WORKERS` - Adjust for your RAM (6-10)
- `TDD_TEST_COVERAGE_THRESHOLD` - Adjust coverage requirement (70-90%)
- `TRUTH_VERIFICATION_THRESHOLD` - Adjust quality gate (0.90-0.98)

---

## 🚀 Quick Reference Commands

### Deployment
```bash
# GitHub Codespaces
Create codespace → Auto-deployed

# Pi 5 / Local Docker
docker-compose up -d

# Cloud (Kubernetes)
kompose convert && kubectl apply -f kubernetes/
```

### Workflow Execution
```bash
# Phase 1: Research
./.agentic/scripts/phase-1-research.sh "your wild idea"

# Phase 2: Formalize
./.agentic/scripts/phase-2-formalize.sh

# Phase 3: SPARC Planning
./.agentic/scripts/phase-3-sparc.sh

# Phase 4: Approve Spec
./.agentic/scripts/phase-4-approve.sh

# Phase 5: TDD Development
./.agentic/scripts/phase-5-develop.sh
```

### Monitoring & Debugging
```bash
# View logs
docker-compose logs -f agentic-dev

# Check container status
docker-compose ps

# Check AgentDB status
docker-compose exec agentic-dev npx agentdb status

# Check MCP server health
curl http://localhost:3000/health

# Monitor memory usage
docker stats agentic-orchestrator
```

---

## 📊 File Size Summary

| File | Size | Purpose |
|------|------|---------|
| AGENTIC-DEV-SERVICE-ARCHITECTURE.md | ~1,000 lines | Main architecture spec |
| 5-PHASE-WORKFLOW-DETAIL.md | ~400 lines | Detailed workflow guide |
| templates/README.md | ~300 lines | Template overview |
| templates/DEPLOYMENT-GUIDE.md | ~500 lines | Deployment guide |
| templates/devcontainer.json | ~200 lines | Codespaces config |
| templates/docker-compose.yml | ~400 lines | Multi-env deployment |
| templates/Dockerfile | ~200 lines | Container image |
| **Total** | **~3,000 lines** | **Complete template** |

---

## 🎓 Learning Path

### Beginner (Never used container-based development)
1. Read: `templates/README.md`
2. Deploy: GitHub Codespaces (easiest)
3. Try: Phase 1 research on a simple idea
4. Learn: Watch logs, understand workflow

### Intermediate (Some Docker experience)
1. Read: `AGENTIC-DEV-SERVICE-ARCHITECTURE.md`
2. Read: `5-PHASE-WORKFLOW-DETAIL.md`
3. Deploy: Local Docker
4. Customize: Add your own agents, adjust configs
5. Try: Complete 5-phase workflow on small project

### Advanced (Ready for production)
1. Read: All documentation
2. Deploy: Raspberry Pi 5 or Cloud
3. Customize: Full workflow customization
4. Integrate: Add your own tools, MCP servers
5. Scale: Multi-container orchestration, K8s

---

## 🤝 Support & Contributing

- **Issues**: Report bugs, request features
- **Discussions**: Ask questions, share workflows
- **Pull Requests**: Contribute improvements
- **Documentation**: Improve guides, add examples

---

## 📝 Version History

- **v4.0** (2025-10-21): 5-Phase Workflow Template
  - Restructured around user's actual creation flow
  - London TDD with continuous swarm iterations
  - Truth verification (≥0.95 threshold)
  - Portable: Codespaces, Pi 5, Docker, Cloud
  - Pattern-driven as optional optimization

---

## 🔗 Quick Links

- [Main Architecture](../AGENTIC-DEV-SERVICE-ARCHITECTURE.md)
- [Workflow Detail](../5-PHASE-WORKFLOW-DETAIL.md)
- [Template README](./README.md)
- [Deployment Guide](./DEPLOYMENT-GUIDE.md)
- [devcontainer.json](./devcontainer.json)
- [docker-compose.yml](./docker-compose.yml)
- [Dockerfile](./Dockerfile)

---

**Ready to start?** Pick a file above and dive in! 🚀
