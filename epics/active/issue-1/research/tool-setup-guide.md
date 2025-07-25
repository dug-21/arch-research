# Architecture Documentation Tools Setup Guide

This guide provides installation and setup instructions for all researched architecture documentation tools.

## Quick Setup Commands

### PlantUML
```bash
# macOS
brew install plantuml

# Ubuntu/Debian
sudo apt-get install plantuml

# Using Java (cross-platform)
wget https://github.com/plantuml/plantuml/releases/download/v1.2024.0/plantuml.jar
java -jar plantuml.jar

# VS Code Extension
code --install-extension jebbs.plantuml
```

### GraphViz
```bash
# macOS
brew install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz

# Windows (Chocolatey)
choco install graphviz

# Python bindings
pip install graphviz
```

### D2
```bash
# macOS
brew install d2

# Linux/WSL
curl -fsSL https://d2lang.com/install.sh | sh -s --

# Using Go
go install oss.terrastruct.com/d2@latest

# VS Code Extension
code --install-extension terrastruct.d2
```

### Structurizr
```bash
# Structurizr CLI
wget https://github.com/structurizr/cli/releases/download/v1.35.0/structurizr-cli-1.35.0.zip
unzip structurizr-cli-1.35.0.zip

# DSL VS Code Extension
code --install-extension structurizr.dsl

# Docker
docker run -it --rm -v $(pwd):/usr/local/structurizr structurizr/cli
```

### Terraform Visualization Tools
```bash
# Blast Radius
pip install blastradius

# Rover
docker run --rm -it -p 9000:9000 -v $(pwd):/src im2nguyen/rover

# Inframap
brew install inframap
# or
go install github.com/cycloidio/inframap@latest

# Terraform Graph (built-in)
terraform graph
```

### BPMN Tools
```bash
# BPMN.io (web-based, no install)
# Visit: https://demo.bpmn.io/

# Camunda Modeler
# Download from: https://camunda.com/download/modeler/

# VS Code Extension
code --install-extension bpmn-io.vs-code-bpmn-io
```

## Detailed Setup Instructions

### PlantUML Setup

#### Prerequisites
- Java 8 or higher
- Graphviz (optional, for better layouts)

#### Installation Options

**Option 1: Standalone JAR**
```bash
mkdir ~/plantuml
cd ~/plantuml
wget https://github.com/plantuml/plantuml/releases/download/v1.2024.0/plantuml.jar
echo 'alias plantuml="java -jar ~/plantuml/plantuml.jar"' >> ~/.bashrc
source ~/.bashrc
```

**Option 2: Package Manager**
```bash
# macOS with Homebrew
brew install plantuml

# Ubuntu/Debian
sudo apt-get update
sudo apt-get install plantuml

# Arch Linux
sudo pacman -S plantuml
```

**Option 3: Docker**
```bash
docker run -v $(pwd):/data plantuml/plantuml
```

#### IDE Integration

**VS Code**
```bash
code --install-extension jebbs.plantuml
```

Settings (`.vscode/settings.json`):
```json
{
  "plantuml.diagramsRoot": "docs/diagrams",
  "plantuml.exportFormat": "png",
  "plantuml.exportSubFolder": false,
  "plantuml.server": "https://www.plantuml.com/plantuml",
  "plantuml.render": "PlantUMLServer"
}
```

**IntelliJ IDEA**
- Install PlantUML Integration plugin from marketplace
- Configure path to plantuml.jar or use bundled version

### GraphViz Setup

#### Installation

**macOS**
```bash
brew install graphviz

# Verify installation
dot -V
```

**Linux**
```bash
# Ubuntu/Debian
sudo apt-get install graphviz

# RedHat/CentOS
sudo yum install graphviz

# Arch
sudo pacman -S graphviz
```

**Windows**
```powershell
# Using Chocolatey
choco install graphviz

# Or download installer from https://graphviz.org/download/
```

#### Python Integration
```bash
pip install graphviz
pip install pygraphviz  # For advanced features
```

Example Python usage:
```python
from graphviz import Digraph

dot = Digraph(comment='Architecture')
dot.node('A', 'Web Server')
dot.node('B', 'Database')
dot.edge('A', 'B', 'queries')
dot.render('architecture', format='png', cleanup=True)
```

### D2 Setup

#### Installation

**macOS/Linux Quick Install**
```bash
# Install script
curl -fsSL https://d2lang.com/install.sh | sh -s --

# Verify
d2 --version
```

**Manual Installation**
```bash
# Download latest release
wget https://github.com/terrastruct/d2/releases/download/v0.6.1/d2-v0.6.1-linux-amd64.tar.gz
tar -xzf d2-v0.6.1-linux-amd64.tar.gz
sudo mv d2-v0.6.1/bin/d2 /usr/local/bin/
```

**From Source**
```bash
go install oss.terrastruct.com/d2@latest
```

#### VS Code Setup
```bash
code --install-extension terrastruct.d2
```

#### Basic Usage
```bash
# Render to SVG
d2 input.d2 output.svg

# Watch mode with live reload
d2 --watch input.d2 output.svg

# Specify layout engine
d2 --layout=elk input.d2 output.svg

# Different themes
d2 --theme=3 input.d2 output.svg
```

### Structurizr Setup

#### Structurizr CLI

**Download and Install**
```bash
# Create directory
mkdir ~/structurizr-cli
cd ~/structurizr-cli

# Download latest CLI
wget https://github.com/structurizr/cli/releases/download/v1.35.0/structurizr-cli-1.35.0.zip
unzip structurizr-cli-1.35.0.zip

# Create alias
echo 'alias structurizr="~/structurizr-cli/structurizr.sh"' >> ~/.bashrc
source ~/.bashrc
```

**Docker Alternative**
```bash
# Create workspace file first
cat > workspace.dsl << 'EOF'
workspace {
    model {
        user = person "User"
        system = softwareSystem "System"
        user -> system "Uses"
    }
    views {
        systemContext system {
            include *
            autoLayout
        }
    }
}
EOF

# Run with Docker
docker run --rm -v $(pwd):/usr/local/structurizr structurizr/cli export -workspace workspace.dsl -format plantuml
```

#### Structurizr Lite (Local Server)

```bash
# Using Docker
docker run -it --rm -p 8080:8080 -v $(pwd):/usr/local/structurizr structurizr/lite

# Access at http://localhost:8080
```

### Terraform Visualization Setup

#### Blast Radius

**Installation**
```bash
# Python pip
pip install blastradius

# Verify
blast-radius --version
```

**Usage**
```bash
# Initialize Terraform first
terraform init

# Serve interactive graph
blast-radius --serve .

# Generate static SVG
blast-radius --svg > infrastructure.svg
```

#### Rover

**Docker Setup**
```bash
# Basic usage
docker run --rm -it -p 9000:9000 -v $(pwd):/src im2nguyen/rover

# With specific plan
terraform plan -out=plan.out
docker run --rm -it -p 9000:9000 -v $(pwd):/src im2nguyen/rover -planPath plan.out
```

**Generate standalone HTML**
```bash
docker run --rm -v $(pwd):/src im2nguyen/rover -genImage
```

#### Inframap

**Installation**
```bash
# macOS
brew install inframap

# From source
go install github.com/cycloidio/inframap@latest

# Generate from state
inframap generate terraform.tfstate > infrastructure.dot
dot -Tpng infrastructure.dot > infrastructure.png
```

### BPMN Tools Setup

#### Camunda Modeler

**Desktop Application**
1. Download from: https://camunda.com/download/modeler/
2. Extract archive
3. Run Camunda Modeler executable

**Configuration**
- Enable plugins: Window → Plugins
- Install linting: https://github.com/camunda/linting-plugin

#### BPMN.io Integration

**For Web Projects**
```bash
npm install bpmn-js
```

**Basic HTML Setup**
```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://unpkg.com/bpmn-js/dist/assets/diagram-js.css">
  <link rel="stylesheet" href="https://unpkg.com/bpmn-js/dist/assets/bpmn-font/css/bpmn.css">
</head>
<body>
  <div id="canvas" style="height: 500px;"></div>
  <script src="https://unpkg.com/bpmn-js/dist/bpmn-modeler.development.js"></script>
  <script>
    var modeler = new BpmnJS({
      container: '#canvas'
    });
  </script>
</body>
</html>
```

## CI/CD Integration

### GitHub Actions

**PlantUML Rendering**
```yaml
name: Render PlantUML
on: [push]
jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Render PlantUML
        uses: grassedge/generate-plantuml-action@v1.5
        with:
          path: docs/diagrams
          message: "Rendered PlantUML diagrams"
```

**D2 Rendering**
```yaml
name: Render D2 Diagrams
on: [push]
jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install D2
        run: curl -fsSL https://d2lang.com/install.sh | sh -s --
      - name: Render diagrams
        run: |
          find . -name "*.d2" -exec d2 {} {}.svg \;
      - uses: actions/upload-artifact@v3
        with:
          name: diagrams
          path: '**/*.svg'
```

### GitLab CI

**Structurizr Export**
```yaml
generate-diagrams:
  image: structurizr/cli:latest
  script:
    - structurizr export -workspace workspace.dsl -format plantuml/mermaid/dot
  artifacts:
    paths:
      - "*.puml"
      - "*.mmd"
      - "*.dot"
```

## Development Environment Setup

### VS Code Extensions Package
```bash
# Install all recommended extensions
code --install-extension jebbs.plantuml \
     --install-extension terrastruct.d2 \
     --install-extension structurizr.dsl \
     --install-extension bpmn-io.vs-code-bpmn-io \
     --install-extension joaompinto.vscode-graphviz \
     --install-extension hashicorp.terraform
```

### Docker Compose for All Tools
```yaml
version: '3.8'
services:
  plantuml:
    image: plantuml/plantuml-server:jetty
    ports:
      - "8080:8080"
  
  structurizr:
    image: structurizr/lite
    ports:
      - "8081:8080"
    volumes:
      - ./structurizr:/usr/local/structurizr
  
  rover:
    image: im2nguyen/rover
    ports:
      - "9000:9000"
    volumes:
      - ./terraform:/src
```

## Troubleshooting

### Common Issues

**PlantUML: "Graphviz not found"**
```bash
# Install Graphviz
sudo apt-get install graphviz
# or
brew install graphviz

# Set GRAPHVIZ_DOT environment variable
export GRAPHVIZ_DOT=/usr/bin/dot
```

**D2: "command not found"**
```bash
# Add to PATH
echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
source ~/.bashrc
```

**Structurizr: "Java not found"**
```bash
# Install Java
sudo apt-get install default-jre
# or
brew install openjdk
```

### Performance Optimization

**PlantUML**
- Use PlantUML Server for better performance
- Enable caching in CI/CD pipelines
- Limit diagram complexity

**GraphViz**
- Use appropriate layout engine (dot, neato, fdp)
- Simplify large graphs with clustering
- Pre-process with gvpr for optimization

**D2**
- Use TALA layout for complex diagrams
- Enable watch mode during development
- Cache rendered outputs

This setup guide ensures all team members can quickly get started with any of the architecture documentation tools.