# Architecture Documentation Quick Start Guide

## Choose Your Methodology

Based on your project needs, select the most appropriate documentation approach:

### 🎨 Mermaid Design System
**Best for:** Visual learners, diagram-driven development, interactive documentation

```bash
# Quick start
npx create-mermaid-docs@latest my-project-docs
cd my-project-docs
npm run dev
```

**First steps:**
1. Create your first architecture diagram: `npm run create:diagram`
2. Generate documentation: `npm run build`
3. View interactive docs: `npm run preview`

### 🏗️ Architectural Documentation (ADR-based)
**Best for:** Enterprise projects, decision tracking, compliance requirements

```bash
# Quick start
npx create-arch-docs@latest my-project-docs
cd my-project-docs
npx adr init
```

**First steps:**
1. Create your first ADR: `npx adr create "Use microservices architecture"`
2. Add architecture views: `npm run create:view`
3. Generate documentation site: `npm run build`

### 📊 Docs-as-Data
**Best for:** Large systems, automated documentation, CI/CD integration

```bash
# Quick start
npx create-docs-as-data@latest my-project-docs
cd my-project-docs
npm run init
```

**First steps:**
1. Define your first component: `npm run create:component`
2. Run queries: `npm run query "components with external dependencies"`
3. Generate reports: `npm run analyze`

### 📦 Modular Documentation
**Best for:** Multi-audience docs, reusable content, progressive disclosure

```bash
# Quick start
npx create-modular-docs@latest my-project-docs
cd my-project-docs
npm run setup
```

**First steps:**
1. Create a concept module: `npm run create:concept "Introduction to Our API"`
2. Create a procedure: `npm run create:procedure "Deploy to Production"`
3. Assemble for developers: `npm run assemble --audience=developer`

## Migration Paths

### From Wiki/Confluence → Any Methodology

1. **Export existing content**
   ```bash
   npx wiki-to-docs export --source=confluence --format=markdown
   ```

2. **Analyze and categorize**
   ```bash
   npx doc-analyzer scan ./exported-docs
   ```

3. **Transform to chosen format**
   ```bash
   # For Mermaid Design System
   npx transform-docs --to=mermaid --auto-diagram
   
   # For ADR-based
   npx transform-docs --to=adr --extract-decisions
   
   # For Docs-as-Data
   npx transform-docs --to=data --create-schemas
   
   # For Modular
   npx transform-docs --to=modular --split-modules
   ```

### From Code Comments → Documentation

1. **Extract documentation from code**
   ```bash
   npx code-doc-extractor scan ./src --output=./raw-docs
   ```

2. **Enhance with architecture context**
   ```bash
   npx enhance-docs --add-context --generate-diagrams
   ```

## Hybrid Approach

Combine multiple methodologies for maximum effectiveness:

```yaml
# docs.config.yaml
methodologies:
  primary: mermaid-design-system  # Visual architecture
  secondary:
    - architectural-documentation  # Decision tracking
    - docs-as-data               # Automated queries
    
integrations:
  - source: mermaid-diagrams
    target: adr-context
  - source: component-data
    target: diagram-generation
```

## Common Commands Reference

| Task | Mermaid | ADR | Docs-as-Data | Modular |
|------|---------|-----|--------------|----------|
| Initialize | `mermaid-docs init` | `adr init` | `docs-as-data init` | `modular-docs init` |
| Create content | `create --type=diagram` | `adr create` | `create --type=component` | `create --type=concept` |
| Build/Generate | `build` | `generate` | `generate --all` | `assemble` |
| Validate | `validate` | `adr validate` | `validate` | `validate` |
| Preview | `preview` | `serve` | `query --ui` | `preview` |

## Best Practices

1. **Start small**: Begin with one methodology and expand
2. **Automate early**: Set up CI/CD validation from day one
3. **Version control**: Treat docs as code - branch, review, merge
4. **Regular updates**: Schedule documentation reviews with code reviews
5. **Measure usage**: Track which docs are most valuable

## Troubleshooting

### "Command not found" errors
```bash
# Install globally
npm install -g @architectural-docs/cli

# Or use npx (recommended)
npx @architectural-docs/cli <command>
```

### Schema validation failures
```bash
# Validate and fix schemas
npx validate-schemas --fix
```

### Broken links in generated docs
```bash
# Check and fix links
npx check-links --fix-relative
```

## Next Steps

1. Join the community: [docs-as-code.community](https://docs-as-code.community)
2. View examples: [github.com/architectural-docs/examples](https://github.com/architectural-docs/examples)
3. Get support: [discord.gg/docs-as-code](https://discord.gg/docs-as-code)

---

**Remember:** The best documentation system is the one your team will actually use. Start simple, iterate often, and let your documentation evolve with your architecture.
