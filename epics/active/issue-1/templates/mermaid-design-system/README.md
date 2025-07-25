# Mermaid Design System Documentation Template

## Overview
This template implements a visual-first approach to architectural documentation using Mermaid diagrams as the primary source of truth.

## Template Structure

```
project-docs/
├── architecture/
│   ├── system-overview.mmd
│   ├── component-diagrams/
│   │   ├── frontend.mmd
│   │   ├── backend.mmd
│   │   └── data-layer.mmd
│   └── flow-diagrams/
│       ├── user-flows.mmd
│       └── data-flows.mmd
├── generated/
│   ├── markdown/
│   ├── html/
│   └── pdf/
├── templates/
│   ├── component.mmd.template
│   ├── sequence.mmd.template
│   └── architecture.mmd.template
└── mermaid.config.json
```

## Quick Start

1. Initialize documentation structure:
   ```bash
   npx mermaid-docs init
   ```

2. Create a new diagram:
   ```bash
   npx mermaid-docs create --type=component --name=auth-service
   ```

3. Generate documentation:
   ```bash
   npx mermaid-docs build
   ```

## Benefits
- Visual-first approach
- Auto-generated documentation from diagrams
- Version control friendly
- Interactive documentation
- Consistent styling

## Integration
- GitHub Actions for auto-generation
- VSCode extension for live preview
- Export to multiple formats (MD, HTML, PDF)
