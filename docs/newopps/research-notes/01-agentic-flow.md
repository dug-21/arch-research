# Agentic Flow - Component Research Notes

**Repository**: https://github.com/ruvnet/agentic-flow

## Overview
Ultra-fast local code transformation and multi-agent orchestration system with cost optimization capabilities.

---

## Named Components

### 1. **Agent Booster**
- **Type**: Code transformation engine
- **Technology**: Rust/WASM
- **Purpose**: Ultra-fast local code transformations with automatic edit detection
- **Performance**: 352x faster than traditional methods, $0 cost
- **Key Capabilities**:
  - Automatic edit detection
  - Local execution without API calls
  - Zero-latency transformations
  - WASM-based portability

### 2. **ReasoningBank**
- **Type**: Persistent learning memory system
- **Technology**: Semantic search with embeddings
- **Purpose**: Enable agents to learn and improve across sessions
- **Performance**: 46% faster execution after initial learning
- **Key Capabilities**:
  - Semantic pattern storage and retrieval
  - Cross-session memory persistence
  - Performance improvement over time
  - Pattern recognition for recurring tasks
- **Integration**: SQLite-based storage with vector embeddings

### 3. **Multi-Model Router**
- **Type**: Intelligent cost optimization system
- **Technology**: Dynamic model selection across 100+ providers
- **Purpose**: Minimize costs while maintaining quality
- **Performance**: 85-99% cost savings
- **Key Capabilities**:
  - Automatic model tier selection (Flagship → Budget → Local)
  - Real-time cost tracking
  - Quality-based routing decisions
  - Support for 100+ LLM providers
- **Supported Providers**: OpenRouter, Google Gemini, Anthropic, DeepSeek, ONNX Runtime

### 4. **QUIC Transport**
- **Type**: Network protocol implementation
- **Technology**: UDP-based protocol with 0-RTT
- **Purpose**: High-speed agent swarm coordination and communication
- **Performance**: 50-70% faster than TCP connections
- **Key Capabilities**:
  - 0-RTT reconnection (zero round-trip time)
  - True multiplexing without head-of-line blocking
  - UDP-based for reduced latency
  - Built-in congestion control
  - Connection migration support
- **Use Cases**:
  - Agent-to-agent communication
  - Swarm coordination
  - Real-time streaming
  - Low-latency task distribution

---

## Agent System (79+ Agents)

### Core Development Agents
- `coder` - Implementation specialist
- `reviewer` - Code quality assurance
- `tester` - Test creation and validation
- `planner` - Strategic planning and architecture
- `researcher` - Information gathering and analysis

### Specialized Domain Agents
- `backend-dev` - Backend/API development
- `mobile-dev` - React Native/mobile development
- `ml-developer` - Machine learning implementation
- `system-architect` - High-level system design
- `cicd-engineer` - CI/CD pipeline management
- `api-docs` - OpenAPI documentation generation

### Swarm Coordination Agents
- `hierarchical-coordinator` - Queen-led swarm coordination
- `mesh-coordinator` - Peer-to-peer network coordination
- `adaptive-coordinator` - Dynamic topology management
- `swarm-memory-manager` - Distributed memory management
- `collective-intelligence-coordinator` - Hive-mind intelligence

### GitHub Integration Agents
- `pr-manager` - Pull request management
- `code-review-swarm` - Multi-agent code review
- `issue-tracker` - Issue management and triage
- `release-manager` - Release coordination
- `workflow-automation` - CI/CD automation

---

## Key Features

### Execution Modes
- **Local Execution**: Full access to 213 MCP tools via Claude Agent SDK
- **Multi-Provider Support**: OpenRouter, Google Gemini, ONNX Runtime (offline)
- **Real-time Streaming**: Live agent output with `--stream` flag
- **Docker Deployment**: Production-ready containerization

### Cost Optimization
- **DeepSeek R1**: $0.55/$2.19 per 1M tokens (input/output)
- **Claude Sonnet**: $3/$15 per 1M tokens
- **Automatic Tier Selection**: Flagship → Budget → Local based on task complexity

### MCP Server Management
- 7 built-in MCP tools
- External integration support
- Claude Agent SDK compatibility

---

## Architectural Patterns

### Swarm Topologies
- **Hierarchical**: Queen-led coordination for complex projects
- **Mesh**: Peer-to-peer for distributed tasks
- **Adaptive**: Dynamic topology based on task requirements

### Semantic Search
- ReasoningBank enables pattern recognition across tasks
- Persistent learning from past executions
- Context-aware task optimization

### Dynamic Model Selection
- Automatic tier-based optimization
- Cost vs. quality tradeoffs
- Real-time provider switching

### 0-RTT Connection (QUIC)
- Eliminates handshake overhead
- Rapid task distribution
- Seamless connection migration

---

## APIs and Interfaces

### CLI Interface
```bash
# Agent spawning with model selection
agentic-flow spawn --agent coder --model deepseek-r1

# Swarm initialization
agentic-flow swarm init --topology mesh --agents 5

# Cost tracking
agentic-flow cost report
```

### MCP Protocol
- Model Context Protocol integration
- Claude Code native support
- Tool-based execution model

### External Integrations
- OpenRouter API
- Google Gemini API
- Anthropic Claude API
- ONNX Runtime for local inference

---

## Performance Characteristics

### Speed Metrics
- **Agent Booster**: 352x faster than traditional methods
- **QUIC Transport**: 50-70% faster than TCP
- **ReasoningBank**: 46% execution improvement after learning

### Cost Metrics
- **Multi-Model Router**: 85-99% cost savings
- **Local Execution**: $0 cost for supported operations
- **DeepSeek Integration**: 5-7x cheaper than GPT-4 class models

### Throughput
- 213 MCP tools available
- 100+ LLM provider support
- Real-time streaming output

---

## Technical Stack

### Languages
- Rust (Agent Booster core)
- TypeScript/JavaScript (CLI and integrations)
- WebAssembly (portability layer)

### Storage
- SQLite (ReasoningBank persistence)
- Vector embeddings for semantic search

### Networking
- QUIC protocol implementation
- UDP-based transport
- HTTP/3 compatibility

### Deployment
- Docker containerization
- NPM/NPX distribution
- Local and cloud execution modes

---

## Integration Points

### Claude Agent SDK
- Full MCP tool access (213 tools)
- Native Claude Code integration
- Agentic workflow support

### OpenRouter
- Multi-provider routing
- Automatic failover
- Cost optimization

### ONNX Runtime
- Offline model execution
- Local inference capabilities
- Privacy-preserving operations

---

## Use Cases

1. **Rapid Code Transformation**: Local edits with zero API cost
2. **Cost-Optimized Development**: Automatic model selection for budget control
3. **Multi-Agent Workflows**: Complex task decomposition and parallel execution
4. **GitHub Automation**: PR management, code review, issue triage
5. **Real-time Collaboration**: QUIC-based low-latency agent coordination

---

## Related Systems

- Integrates with **claude-flow** for enhanced orchestration
- Uses **ruv-FANN** for neural decision-making
- Leverages **QUIC** from QuDAG protocol
- Compatible with **DAA SDK** for autonomous operations

---

## References

- Repository: https://github.com/ruvnet/agentic-flow
- Documentation: See repository README and docs/
- Performance benchmarks: Agent Booster (352x), QUIC (50-70% faster), ReasoningBank (46% improvement)
