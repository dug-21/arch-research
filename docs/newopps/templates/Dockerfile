# Agentic Development - 5-Phase Workflow Container
# Base: Node.js 20 on Debian (for claude-flow, goalie, agentdb)

FROM node:20-bullseye-slim

# Metadata
LABEL maintainer="agentic-dev"
LABEL description="Portable 5-phase development workflow with SPARC + London TDD + Truth Verification"
LABEL version="1.0.0"

# Arguments
ARG CLAUDE_FLOW_VERSION=alpha
ARG NODE_VERSION=20

# ─────────────────────────────────────────────────────────────────
# SYSTEM DEPENDENCIES
# ─────────────────────────────────────────────────────────────────

RUN apt-get update && apt-get install -y \
    # Build tools
    build-essential \
    python3 \
    python3-pip \
    # Git
    git \
    # GitHub CLI (for gh integration)
    curl \
    && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh \
    # Docker CLI (for docker-in-docker if needed)
    && curl -fsSL https://get.docker.com | sh \
    # Cleanup
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ─────────────────────────────────────────────────────────────────
# GLOBAL NPM PACKAGES
# ─────────────────────────────────────────────────────────────────

RUN npm install -g \
    # Claude-Flow Orchestration
    claude-flow@${CLAUDE_FLOW_VERSION} \
    # Goalie GOAP Search
    goalie \
    # AgentDB Vector Database
    agentdb \
    # Development Tools
    typescript \
    ts-node \
    nodemon \
    # Testing
    jest \
    @types/jest \
    # Linting
    eslint \
    prettier

# ─────────────────────────────────────────────────────────────────
# WORKSPACE SETUP
# ─────────────────────────────────────────────────────────────────

# Create workspace directory
WORKDIR /workspace

# Create data directories
RUN mkdir -p /data /app/logs /app/agents /patterns \
    && chmod 777 /data /app/logs

# ─────────────────────────────────────────────────────────────────
# AGENT DEFINITIONS (64+ .md files)
# ─────────────────────────────────────────────────────────────────

# Copy agent definitions (will be overridden by volume mount)
COPY .agentic/agents /app/agents

# ─────────────────────────────────────────────────────────────────
# WORKFLOW SCRIPTS
# ─────────────────────────────────────────────────────────────────

# Copy workflow scripts
COPY .agentic/scripts /app/scripts
RUN chmod +x /app/scripts/*.sh

# Add scripts to PATH
ENV PATH="/app/scripts:${PATH}"

# ─────────────────────────────────────────────────────────────────
# MCP SERVER SETUP
# ─────────────────────────────────────────────────────────────────

# Create MCP server directory
RUN mkdir -p /app/mcp

# MCP server start script
COPY .agentic/config/mcp-start.sh /app/mcp/start.sh
RUN chmod +x /app/mcp/start.sh

# ─────────────────────────────────────────────────────────────────
# AGENTDB INITIALIZATION
# ─────────────────────────────────────────────────────────────────

# Initialize AgentDB (creates schema)
RUN mkdir -p /data && \
    npx agentdb init --path /data/agentdb.db

# ─────────────────────────────────────────────────────────────────
# ENVIRONMENT CONFIGURATION
# ─────────────────────────────────────────────────────────────────

# Set environment variables (defaults, overridden by docker-compose)
ENV NODE_ENV=development
ENV WORKSPACE_ROOT=/workspace
ENV AGENTDB_PATH=/data/agentdb.db
ENV AGENTIC_WORKFLOW_VERSION=5-phase-v1.0

# ─────────────────────────────────────────────────────────────────
# HEALTH CHECK ENDPOINT
# ─────────────────────────────────────────────────────────────────

# Simple health check server (Node.js)
COPY .agentic/config/health-server.js /app/health-server.js

# ─────────────────────────────────────────────────────────────────
# STARTUP SCRIPT
# ─────────────────────────────────────────────────────────────────

# Main startup script
COPY .agentic/scripts/start.sh /app/start.sh
RUN chmod +x /app/start.sh

# ─────────────────────────────────────────────────────────────────
# EXPOSE PORTS
# ─────────────────────────────────────────────────────────────────

# MCP Server
EXPOSE 3000

# AgentDB Monitoring API
EXPOSE 3001

# Swagger UI (optional)
EXPOSE 8080

# ─────────────────────────────────────────────────────────────────
# ENTRYPOINT & CMD
# ─────────────────────────────────────────────────────────────────

# Keep container running + start services
CMD ["/app/start.sh"]

# ─────────────────────────────────────────────────────────────────
# BUILD INSTRUCTIONS
# ─────────────────────────────────────────────────────────────────

# Build:
#   docker build -t agentic-dev/5-phase-workflow:latest .

# Run standalone:
#   docker run -it -p 3000:3000 -v $(pwd):/workspace agentic-dev/5-phase-workflow:latest

# Run with docker-compose:
#   docker-compose up -d

# ─────────────────────────────────────────────────────────────────
# VOLUME MOUNT POINTS (defined in docker-compose.yml)
# ─────────────────────────────────────────────────────────────────

# /workspace         - Project files (bind mount from host)
# /data              - AgentDB database (persistent volume)
# /root/.config/gh   - GitHub CLI config (persistent volume)
# /app/agents        - Agent definitions (bind mount from host, read-only)
# /patterns          - Proven patterns library (bind mount from host)
# /app/logs          - Application logs (persistent volume)
