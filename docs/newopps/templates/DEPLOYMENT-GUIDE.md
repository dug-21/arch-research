# Agentic Development Template - Deployment Guide

Complete guide for deploying the 5-Phase Creation Workflow in any environment.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [GitHub Codespaces](#github-codespaces)
3. [Raspberry Pi 5](#raspberry-pi-5)
4. [Local Docker](#local-docker)
5. [Cloud Deployment](#cloud-deployment)
6. [Environment Variables](#environment-variables)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

**Choose your environment and jump to the relevant section:**

- 🚀 **GitHub Codespaces**: Click "Code" → "Create codespace" → Done!
- 🍓 **Raspberry Pi 5**: Install Docker → `docker-compose up -d` → Done!
- 💻 **Local Docker**: Clone → `docker-compose up` → Done!
- ☁️ **Cloud (AWS/GCP/Azure)**: Convert to K8s → Deploy → Done!

---

## GitHub Codespaces

### Prerequisites
- GitHub account
- Repository with this template
- Anthropic API key (set in Codespaces secrets)

### Setup (One-Time)

1. **Add Anthropic API Key to Codespaces Secrets**
   ```
   GitHub Repo → Settings → Secrets and variables → Codespaces
   → New repository secret
   Name: ANTHROPIC_API_KEY
   Value: sk-ant-...
   ```

2. **Create Codespace**
   ```
   GitHub Repo → Code button → Codespaces tab
   → Create codespace on main
   ```

3. **Wait for Container Build** (2-3 minutes first time)
   - Dockerfile builds automatically
   - devcontainer.json configures VS Code
   - MCP servers start automatically
   - AgentDB initializes

4. **Verify Installation**
   ```bash
   # In Codespaces terminal
   npx claude-flow --version
   npx goalie --version
   npx agentdb status
   ```

### Usage

#### Phase 1: Research
```bash
./.agentic/scripts/phase-1-research.sh "AI-powered API documentation from code comments"
```

#### Phase 2: Formalize
```bash
./.agentic/scripts/phase-2-formalize.sh
# Interactive session with Collective Intelligence agent
```

#### Phase 3: SPARC Planning
```bash
./.agentic/scripts/phase-3-sparc.sh
# Generates: specification.md, pseudocode.md, architecture.md
```

#### Phase 4: Approve Spec
```bash
./.agentic/scripts/phase-4-approve.sh
# Review SPARC spec → Approve or request changes
```

#### Phase 5: TDD Development
```bash
./.agentic/scripts/phase-5-develop.sh
# Launches continuous swarm (runs until completion)
# Monitor: docker-compose logs -f agentic-dev
```

### Codespaces-Specific Features

- ✅ **GitHub Token**: Auto-configured from Codespaces
- ✅ **Port Forwarding**: MCP server (3000) auto-forwarded
- ✅ **VS Code Extensions**: Claude Code, GitHub PR, Jest auto-installed
- ✅ **Persistent Storage**: AgentDB persists across rebuilds

### Stopping/Restarting

```bash
# Stop container
docker-compose down

# Restart container
docker-compose up -d

# Full rebuild (if template updated)
Codespace → Rebuild Container
```

---

## Raspberry Pi 5

### Prerequisites
- Raspberry Pi 5 (16GB RAM recommended, 8GB minimum)
- Raspberry Pi OS (64-bit, Debian-based)
- 256GB+ storage (SSD/NVMe recommended)
- Docker installed

### Install Docker (if not installed)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh

# Add user to docker group (avoid sudo)
sudo usermod -aG docker $USER

# Logout and login for group change to take effect
logout
```

### Install Docker Compose

```bash
# Install docker-compose v2
sudo apt install docker-compose-plugin

# Verify
docker compose version
```

### Setup Storage (Recommended)

```bash
# Mount external SSD for AgentDB data (recommended for performance)
sudo mkdir -p /mnt/storage

# Mount external drive (replace /dev/sda1 with your drive)
sudo mount /dev/sda1 /mnt/storage

# Make mount persistent (add to /etc/fstab)
echo "/dev/sda1 /mnt/storage ext4 defaults 0 2" | sudo tee -a /etc/fstab

# Create data directories
sudo mkdir -p /mnt/storage/{agentdb,gh-config,logs}
sudo chown -R $USER:$USER /mnt/storage
```

### Clone Template Repository

```bash
# Clone your project (or create from template)
git clone https://github.com/yourusername/your-project.git
cd your-project
```

### Configure Environment

```bash
# Copy example .env file
cp .env.example .env

# Edit .env
nano .env
```

**.env file** (for Pi 5):
```bash
# API Keys
ANTHROPIC_API_KEY=sk-ant-...
GITHUB_TOKEN=ghp_...

# Storage Paths (using external SSD)
AGENTDB_DATA_PATH=/mnt/storage/agentdb
GH_CONFIG_PATH=/mnt/storage/gh-config
LOGS_PATH=/mnt/storage/logs

# Resource Limits (12GB RAM for 16GB Pi)
MEMORY_LIMIT=12g
CPU_LIMIT=3.0
```

### Start Container

```bash
# Build and start (first time)
docker compose up -d --build

# View logs
docker compose logs -f agentic-dev

# Check status
docker compose ps
```

### Usage on Pi 5

Same as Codespaces (use scripts in `.agentic/scripts/`):

```bash
# Phase 1: Research
./.agentic/scripts/phase-1-research.sh "your wild idea"

# Phase 2-5: Same as Codespaces
```

### Pi 5-Specific Optimizations

**Memory Management**:
```bash
# Monitor memory usage
docker stats agentic-orchestrator

# If running out of memory, reduce parallel workers
# Edit docker-compose.yml:
# MAX_PARALLEL_WORKERS=6  (instead of 10)
```

**Performance Tuning**:
```bash
# Use SSD for AgentDB (not SD card)
# Enable swap if needed (8GB Pi only)
sudo swapon --show
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Auto-Start on Boot

```bash
# Enable Docker to start on boot
sudo systemctl enable docker

# Create systemd service for agentic-dev
sudo nano /etc/systemd/system/agentic-dev.service
```

**/etc/systemd/system/agentic-dev.service**:
```ini
[Unit]
Description=Agentic Development Service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/pi/your-project
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
User=pi

[Install]
WantedBy=multi-user.target
```

```bash
# Enable service
sudo systemctl enable agentic-dev.service

# Start now
sudo systemctl start agentic-dev.service
```

---

## Local Docker

### Prerequisites
- Docker Desktop (Mac/Windows) or Docker Engine (Linux)
- 16GB+ RAM recommended (8GB minimum)
- Anthropic API key

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/your-project.git
cd your-project

# Copy environment file
cp .env.example .env

# Edit .env (add API keys)
nano .env  # or use your favorite editor
```

**.env file** (for local Docker):
```bash
# API Keys
ANTHROPIC_API_KEY=sk-ant-...
GITHUB_TOKEN=ghp_...

# Storage Paths (local data directory)
AGENTDB_DATA_PATH=./data/agentdb
GH_CONFIG_PATH=./data/gh-config
LOGS_PATH=./data/logs

# Resource Limits (adjust based on your machine)
MEMORY_LIMIT=12g
CPU_LIMIT=3.0
```

### Start Container

```bash
# Build and start
docker compose up -d --build

# View logs
docker compose logs -f agentic-dev

# Open VS Code with Dev Containers extension
code .
# Then: Command Palette → "Dev Containers: Reopen in Container"
```

### Usage

Same workflow as Codespaces/Pi 5.

### Stopping

```bash
# Stop container
docker compose down

# Stop and remove volumes (full cleanup)
docker compose down -v
```

---

## Cloud Deployment

### AWS (ECS / EKS)

#### Option 1: ECS with Docker Compose
```bash
# Install ECS CLI
sudo curl -Lo /usr/local/bin/ecs-cli \
  https://amazon-ecs-cli.s3.amazonaws.com/ecs-cli-linux-amd64-latest
sudo chmod +x /usr/local/bin/ecs-cli

# Configure ECS
ecs-cli configure --cluster agentic-dev \
  --region us-east-1 \
  --default-launch-type FARGATE

# Deploy
ecs-cli compose up
```

#### Option 2: EKS with Kubernetes
```bash
# Convert docker-compose to Kubernetes manifests
kompose convert

# Create EKS cluster
eksctl create cluster --name agentic-dev --region us-east-1

# Deploy
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f persistent-volume.yaml
```

### GCP (Cloud Run / GKE)

#### Cloud Run (Serverless)
```bash
# Build image
docker build -t gcr.io/PROJECT_ID/agentic-dev .

# Push to GCR
docker push gcr.io/PROJECT_ID/agentic-dev

# Deploy to Cloud Run
gcloud run deploy agentic-dev \
  --image gcr.io/PROJECT_ID/agentic-dev \
  --platform managed \
  --region us-central1 \
  --memory 12Gi \
  --cpu 4 \
  --set-env-vars ANTHROPIC_API_KEY=sk-ant-...
```

#### GKE (Kubernetes)
```bash
# Create GKE cluster
gcloud container clusters create agentic-dev \
  --zone us-central1-a \
  --num-nodes 2 \
  --machine-type n1-standard-4

# Deploy
kubectl apply -f kubernetes/
```

### Azure (Container Instances / AKS)

#### Container Instances
```bash
# Create resource group
az group create --name agentic-dev-rg --location eastus

# Deploy container
az container create \
  --resource-group agentic-dev-rg \
  --name agentic-dev \
  --image agentic-dev/5-phase-workflow:latest \
  --cpu 4 \
  --memory 12 \
  --environment-variables \
    ANTHROPIC_API_KEY=sk-ant-... \
    GITHUB_TOKEN=ghp_...
```

#### AKS (Kubernetes)
```bash
# Create AKS cluster
az aks create \
  --resource-group agentic-dev-rg \
  --name agentic-dev-cluster \
  --node-count 2 \
  --node-vm-size Standard_D4s_v3

# Get credentials
az aks get-credentials --resource-group agentic-dev-rg --name agentic-dev-cluster

# Deploy
kubectl apply -f kubernetes/
```

---

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude | `sk-ant-api03-...` |

### Optional (with defaults)

| Variable | Default | Description |
|----------|---------|-------------|
| `GITHUB_TOKEN` | - | GitHub personal access token |
| `AGENTDB_DATA_PATH` | `./data/agentdb` | AgentDB storage path |
| `GH_CONFIG_PATH` | `./data/gh-config` | GitHub CLI config path |
| `LOGS_PATH` | `./data/logs` | Application logs path |
| `MAX_PARALLEL_WORKERS` | `10` | Max parallel TDD workers |
| `TDD_TEST_COVERAGE_THRESHOLD` | `80` | Minimum test coverage % |
| `TRUTH_VERIFICATION_THRESHOLD` | `0.95` | Truth verification threshold |
| `MEMORY_LIMIT` | `12g` | Docker memory limit |
| `CPU_LIMIT` | `3.0` | Docker CPU limit |

### Phase-Specific

| Variable | Default | Description |
|----------|---------|-------------|
| `ENABLE_PHASE_1_RESEARCH` | `true` | Enable wild idea research |
| `ENABLE_PHASE_2_FORMALIZE` | `true` | Enable scope formalization |
| `ENABLE_PHASE_3_SPARC` | `true` | Enable SPARC planning |
| `ENABLE_PHASE_4_APPROVAL` | `true` | Enable human approval gate |
| `ENABLE_PHASE_5_TDD` | `true` | Enable London TDD development |

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker compose logs agentic-dev

# Common issues:
# 1. API key not set
docker compose config  # Verify ANTHROPIC_API_KEY

# 2. Port already in use
lsof -i :3000  # Check what's using port 3000
# Kill process or change port in docker-compose.yml

# 3. Insufficient memory
docker info | grep Memory  # Check available RAM
# Reduce MEMORY_LIMIT in docker-compose.yml
```

### MCP Server Not Responding

```bash
# Check MCP server status
curl http://localhost:3000/health

# Restart MCP server
docker compose restart agentic-dev

# View MCP logs
docker compose logs -f agentic-dev | grep MCP
```

### AgentDB Issues

```bash
# Check AgentDB status
docker compose exec agentic-dev npx agentdb status

# Reinitialize AgentDB (WARNING: destroys data)
docker compose exec agentic-dev npx agentdb init --path /data/agentdb.db --force
```

### Out of Memory

```bash
# Check memory usage
docker stats agentic-orchestrator

# Solutions:
# 1. Reduce parallel workers
# Edit docker-compose.yml: MAX_PARALLEL_WORKERS=6

# 2. Increase Docker memory limit
# Docker Desktop → Settings → Resources → Memory → 16GB

# 3. Add swap (Pi 5 only)
sudo fallocate -l 8G /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### GitHub Authentication

```bash
# Login to GitHub CLI
docker compose exec agentic-dev gh auth login

# Verify authentication
docker compose exec agentic-dev gh auth status
```

### Permission Errors

```bash
# Fix file permissions (host)
sudo chown -R $USER:$USER ./data

# Fix permissions (container)
docker compose exec -u root agentic-dev chown -R root:root /data
```

---

## Next Steps

After deployment:

1. **Run Phase 1**: `./.agentic/scripts/phase-1-research.sh "your idea"`
2. **Monitor Logs**: `docker compose logs -f`
3. **Check Health**: `curl http://localhost:3000/health`
4. **Open Claude Code**: Connect to MCP server on port 3000

---

## Support

- **Documentation**: See `5-PHASE-WORKFLOW-DETAIL.md` for workflow details
- **Issues**: https://github.com/yourusername/your-project/issues
- **Template**: https://github.com/yourusername/agentic-dev-template

---

**Ready to create?** Pick your environment and follow the guide above! 🚀
