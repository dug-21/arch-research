# Architecture Methodologies Implementation Guide

## Overview

This guide provides practical implementation details for the five architecture methodologies analyzed: C4 Model, ArchiMate, Viewpoints & Perspectives, SPARC, and Structurizr. Each methodology has specific tooling requirements, workflows, and integration points.

## 1. C4 Model Implementation

### Tooling Setup

#### PlantUML Integration
```bash
# Install PlantUML
brew install plantuml  # macOS
apt-get install plantuml  # Ubuntu

# VS Code Extension
code --install-extension jebbs.plantuml

# IntelliJ Plugin
# Install "PlantUML integration" from marketplace
```

#### C4-PlantUML Library Setup
```bash
# Clone the C4-PlantUML library
git clone https://github.com/plantuml-stdlib/C4-PlantUML.git

# Or use remote includes in diagrams
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml
```

### CI/CD Integration

#### GitLab CI Pipeline
```yaml
generate-c4-diagrams:
  stage: documentation
  image: plantuml/plantuml:latest
  script:
    - mkdir -p output/diagrams
    - plantuml -tpng -o output/diagrams "docs/architecture/c4/*.puml"
  artifacts:
    paths:
      - output/diagrams/
    expire_in: 1 week
```

#### GitHub Actions
```yaml
name: Generate C4 Diagrams
on:
  push:
    paths:
      - 'docs/architecture/c4/**/*.puml'

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate diagrams
        uses: cloudbees/plantuml-github-action@master
        with:
          args: -tpng docs/architecture/c4/*.puml
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: c4-diagrams
          path: '**/*.png'
```

### IDE Support

#### VS Code Configuration
```json
{
  "plantuml.server": "https://www.plantuml.com/plantuml",
  "plantuml.render": "PlantUMLServer",
  "plantuml.exportFormat": "png",
  "plantuml.exportOutDir": "./out/diagrams",
  "plantuml.includepaths": [
    "./c4-includes"
  ]
}
```

### Version Control Best Practices
```bash
# Directory structure
architecture/
├── c4/
│   ├── level1-context/
│   │   ├── system-context.puml
│   │   └── README.md
│   ├── level2-container/
│   │   ├── container-diagram.puml
│   │   └── README.md
│   ├── level3-component/
│   │   ├── api-components.puml
│   │   └── README.md
│   └── level4-code/
│       ├── class-diagrams.puml
│       └── README.md
└── exports/
    └── png/
```

## 2. ArchiMate Implementation

### Tool Setup

#### Archi - Open Source ArchiMate Tool
```bash
# Download from https://www.archimatetool.com/
# Available for Windows, macOS, Linux

# Command line usage
archi -consoleLog -console -nosplash \
  -application com.archimatetool.commandline.app \
  --modelrepository.loadModel "mymodel.archimate" \
  --html.createReport "output/"
```

#### Commercial Tools
- **BiZZdesign Enterprise Studio**
- **Sparx Enterprise Architect**
- **Visual Paradigm**

### Exchange Format Integration

#### Open Exchange Format
```xml
<!-- Model exchange template -->
<?xml version="1.0" encoding="UTF-8"?>
<model xmlns="http://www.opengroup.org/xsd/archimate/3.0/" 
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <name>Architecture Model</name>
  <documentation>Model documentation</documentation>
  <elements>
    <!-- Elements here -->
  </elements>
  <relationships>
    <!-- Relationships here -->
  </relationships>
</model>
```

### CI/CD Pipeline Integration

```yaml
# Generate HTML documentation from ArchiMate model
archimate-docs:
  stage: documentation
  image: 
    name: archimatetool/archi-cli:latest
    entrypoint: [""]
  script:
    - |
      xvfb-run -a /opt/Archi/Archi \
        -consoleLog -console -nosplash \
        -application com.archimatetool.commandline.app \
        --modelrepository.loadModel "architecture/model.archimate" \
        --html.createReport "output/archimate-docs/"
  artifacts:
    paths:
      - output/archimate-docs/
```

### Collaboration Workflow

```bash
# Git integration for ArchiMate models
# Use Git LFS for binary formats
git lfs track "*.archimate"
git add .gitattributes

# For text-based exchange format
*.archimate merge=ours
*.xml diff=xml
```

## 3. Viewpoints & Perspectives Implementation

### Framework Setup

```yaml
# viewpoints-config.yaml
project:
  name: "E-Commerce Platform"
  version: "1.0.0"
  
viewpoints:
  - id: functional
    name: "Functional Viewpoint"
    template: templates/functional-viewpoint.md
    models:
      - type: component-diagram
        tool: plantuml
      - type: sequence-diagram
        tool: mermaid
  
  - id: deployment
    name: "Deployment Viewpoint"
    template: templates/deployment-viewpoint.md
    models:
      - type: deployment-diagram
        tool: drawio
      - type: infrastructure-code
        tool: terraform

perspectives:
  - id: security
    name: "Security Perspective"
    checklist: checklists/security-perspective.md
    applies_to: [functional, deployment, information]
```

### Documentation Generation

```python
# generate_viewpoints.py
import yaml
import jinja2
import os

def generate_viewpoint_docs(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates')
    )
    
    for viewpoint in config['viewpoints']:
        template = env.get_template(viewpoint['template'])
        output = template.render(viewpoint=viewpoint)
        
        output_path = f"docs/viewpoints/{viewpoint['id']}.md"
        with open(output_path, 'w') as f:
            f.write(output)
```

### Stakeholder-Specific Views

```javascript
// viewpoint-router.js
const express = require('express');
const router = express.Router();

// Route different stakeholders to appropriate views
router.get('/architecture/:stakeholder', (req, res) => {
  const { stakeholder } = req.params;
  
  const viewpointMapping = {
    'developer': ['functional', 'information', 'development'],
    'operations': ['deployment', 'operational', 'concurrency'],
    'security': ['security-perspective', 'deployment'],
    'business': ['functional', 'information']
  };
  
  const relevantViewpoints = viewpointMapping[stakeholder] || [];
  res.render('architecture-portal', { 
    stakeholder, 
    viewpoints: relevantViewpoints 
  });
});
```

## 4. SPARC Implementation

### Project Structure

```bash
sparc-project/
├── 01-specification/
│   ├── requirements.yaml
│   ├── user-stories.md
│   └── constraints.md
├── 02-pseudocode/
│   ├── algorithms/
│   ├── workflows/
│   └── domain-logic/
├── 03-architecture/
│   ├── system-design.md
│   ├── component-diagrams/
│   └── deployment-arch.yaml
├── 04-refinement/
│   ├── optimizations.md
│   ├── security-measures.yaml
│   └── performance-tuning.md
└── 05-code/
    ├── implementation/
    ├── tests/
    └── infrastructure/
```

### Automation Scripts

```python
# sparc_validator.py
import os
import yaml
from pathlib import Path

class SPARCValidator:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        
    def validate_structure(self):
        required_dirs = [
            '01-specification',
            '02-pseudocode',
            '03-architecture',
            '04-refinement',
            '05-code'
        ]
        
        missing = []
        for dir in required_dirs:
            if not (self.project_root / dir).exists():
                missing.append(dir)
        
        return len(missing) == 0, missing
    
    def validate_traceability(self):
        # Check that requirements are traced through all phases
        specs = self.load_specifications()
        pseudocode = self.check_pseudocode_coverage(specs)
        architecture = self.check_architecture_coverage(specs)
        
        return {
            'specification_count': len(specs),
            'pseudocode_coverage': pseudocode,
            'architecture_coverage': architecture
        }
```

### CI/CD Integration

```yaml
# SPARC methodology validation
sparc-validation:
  stage: validate
  script:
    - python sparc_validator.py .
    - python generate_sparc_report.py
  artifacts:
    reports:
      junit: sparc-validation-report.xml
    paths:
      - sparc-report.html

# Generate documentation from SPARC phases
sparc-docs:
  stage: documentation
  script:
    - pip install mkdocs mkdocs-material
    - python compile_sparc_docs.py
    - mkdocs build
  artifacts:
    paths:
      - site/
```

## 5. Structurizr Implementation

### Structurizr CLI Setup

```bash
# Install Structurizr CLI
wget https://github.com/structurizr/cli/releases/latest/download/structurizr-cli.zip
unzip structurizr-cli.zip

# Validate workspace
./structurizr-cli validate -workspace workspace.dsl

# Generate PlantUML
./structurizr-cli export -workspace workspace.dsl -format plantuml

# Push to Structurizr cloud
./structurizr-cli push -workspace workspace.dsl \
  -id 12345 \
  -key your-api-key \
  -secret your-api-secret
```

### Local Development with Docker

```dockerfile
# Dockerfile for Structurizr Lite
FROM structurizr/lite:latest

COPY workspace.dsl /usr/local/structurizr/
COPY workspace.json /usr/local/structurizr/

EXPOSE 8080
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  structurizr:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./workspace.dsl:/usr/local/structurizr/workspace.dsl
    environment:
      - STRUCTURIZR_WORKSPACE_FILENAME=workspace.dsl
```

### API Integration

```javascript
// structurizr-client.js
const axios = require('axios');
const crypto = require('crypto');

class StructurizrClient {
  constructor(apiKey, apiSecret, workspaceId) {
    this.apiKey = apiKey;
    this.apiSecret = apiSecret;
    this.workspaceId = workspaceId;
    this.baseUrl = 'https://api.structurizr.com';
  }
  
  async getWorkspace() {
    const path = `/workspace/${this.workspaceId}`;
    const nonce = Date.now();
    const method = 'GET';
    
    const hmac = crypto.createHmac('sha256', this.apiSecret);
    hmac.update(`${method}${path}${nonce}`);
    const signature = hmac.digest('hex');
    
    const response = await axios.get(`${this.baseUrl}${path}`, {
      headers: {
        'X-Authorization': `${this.apiKey}:${signature}`,
        'Nonce': nonce
      }
    });
    
    return response.data;
  }
  
  async updateWorkspace(workspace) {
    // Implementation for updating workspace
  }
}
```

### GitHub Actions Integration

```yaml
name: Update Structurizr
on:
  push:
    paths:
      - 'architecture/workspace.dsl'

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Validate DSL
        run: |
          wget -q https://github.com/structurizr/cli/releases/latest/download/structurizr-cli.zip
          unzip -q structurizr-cli.zip
          ./structurizr-cli validate -workspace architecture/workspace.dsl
      
      - name: Generate Diagrams
        run: |
          ./structurizr-cli export -workspace architecture/workspace.dsl \
            -format plantuml -output docs/diagrams
          
      - name: Push to Structurizr
        env:
          STRUCTURIZR_API_KEY: ${{ secrets.STRUCTURIZR_API_KEY }}
          STRUCTURIZR_API_SECRET: ${{ secrets.STRUCTURIZR_API_SECRET }}
        run: |
          ./structurizr-cli push -workspace architecture/workspace.dsl \
            -id ${{ secrets.STRUCTURIZR_WORKSPACE_ID }} \
            -key $STRUCTURIZR_API_KEY \
            -secret $STRUCTURIZR_API_SECRET
```

## Cross-Methodology Integration

### Unified Documentation Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - generate
  - publish

variables:
  ARCHITECTURE_OUTPUT: "architecture-docs"

validate-all:
  stage: validate
  parallel:
    matrix:
      - METHODOLOGY: [c4, archimate, structurizr, sparc]
  script:
    - ./scripts/validate-${METHODOLOGY}.sh

generate-docs:
  stage: generate
  script:
    # C4 Model
    - plantuml -tsvg -o $ARCHITECTURE_OUTPUT/c4 "architecture/c4/**/*.puml"
    
    # Structurizr
    - structurizr-cli export -workspace architecture/workspace.dsl \
        -format mermaid -output $ARCHITECTURE_OUTPUT/structurizr
    
    # ArchiMate
    - archi-cli --modelrepository.loadModel "architecture/model.archimate" \
        --html.createReport "$ARCHITECTURE_OUTPUT/archimate/"
    
    # SPARC
    - python generate_sparc_docs.py -o $ARCHITECTURE_OUTPUT/sparc
    
    # Viewpoints
    - python generate_viewpoints.py -o $ARCHITECTURE_OUTPUT/viewpoints
    
  artifacts:
    paths:
      - $ARCHITECTURE_OUTPUT/

publish-docs:
  stage: publish
  dependencies:
    - generate-docs
  script:
    - npm install -g @architecturetool/publisher
    - arch-publish --input $ARCHITECTURE_OUTPUT --output public/
  artifacts:
    paths:
      - public/
```

### Methodology Comparison Matrix

| Aspect | C4 Model | ArchiMate | Viewpoints | SPARC | Structurizr |
|--------|----------|-----------|------------|-------|-------------|
| **Primary Format** | PlantUML | XML/Binary | Markdown/Various | Mixed | DSL |
| **Version Control** | Excellent | Good (XML) | Excellent | Excellent | Excellent |
| **CI/CD Integration** | Easy | Moderate | Easy | Easy | Easy |
| **Tool Lock-in** | Low | Medium | Low | None | Low |
| **Collaboration** | Git-based | Tool-specific | Git-based | Git-based | Git/Cloud |
| **Learning Curve** | Low | High | Medium | Low | Low |
| **Automation** | High | Medium | High | High | High |
| **Export Options** | Many | Many | Flexible | N/A | Many |

## Best Practices

### 1. Version Control
- Use text-based formats where possible
- Implement semantic versioning for architecture documents
- Use Git LFS for binary formats
- Create meaningful commit messages for architecture changes

### 2. Automation
- Automate diagram generation in CI/CD
- Implement validation checks for consistency
- Auto-generate documentation from models
- Create architecture decision records (ADRs)

### 3. Tooling
- Standardize on tools across teams
- Provide IDE plugins/extensions
- Create project templates
- Maintain tool configuration in version control

### 4. Collaboration
- Define clear ownership of architecture artifacts
- Implement review processes for changes
- Create stakeholder-specific views
- Maintain traceability between artifacts

### 5. Integration
- Link architecture to code through annotations
- Generate code stubs from models where appropriate
- Validate implementation against architecture
- Maintain bi-directional traceability