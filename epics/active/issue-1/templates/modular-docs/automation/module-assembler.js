#!/usr/bin/env node

/**
 * Modular Documentation Assembler
 * Dynamically assembles documentation from modules based on audience and context
 */

const fs = require('fs').promises;
const path = require('path');
const yaml = require('js-yaml');
const matter = require('gray-matter');
const marked = require('marked');
const Handlebars = require('handlebars');

class ModuleAssembler {
  constructor(config = {}) {
    this.config = {
      modulesDir: config.modulesDir || './modules',
      assembliesDir: config.assembliesDir || './assemblies',
      outputDir: config.outputDir || './output',
      metadataDir: config.metadataDir || './metadata',
      ...config
    };
    
    this.modules = new Map();
    this.metadata = {};
    this.assemblies = new Map();
  }

  async initialize() {
    // Load all modules
    await this.loadModules();
    
    // Load metadata
    await this.loadMetadata();
    
    // Load assembly definitions
    await this.loadAssemblies();
  }

  async loadModules() {
    const moduleTypes = ['concepts', 'procedures', 'reference', 'tutorials'];
    
    for (const type of moduleTypes) {
      const dir = path.join(this.config.modulesDir, type);
      
      try {
        const files = await fs.readdir(dir);
        
        for (const file of files) {
          if (file.endsWith('.md')) {
            const content = await fs.readFile(path.join(dir, file), 'utf8');
            const { data: frontmatter, content: body } = matter(content);
            
            const moduleId = frontmatter.id || path.basename(file, '.md');
            
            this.modules.set(moduleId, {
              id: moduleId,
              type,
              file,
              path: path.join(dir, file),
              frontmatter,
              content: body,
              dependencies: this.extractDependencies(frontmatter)
            });
          }
        }
      } catch (error) {
        console.warn(`Module type directory not found: ${type}`);
      }
    }
    
    console.log(`📦 Loaded ${this.modules.size} modules`);
  }

  extractDependencies(frontmatter) {
    const deps = [];
    
    if (frontmatter.prerequisites) {
      if (frontmatter.prerequisites.concepts) {
        deps.push(...frontmatter.prerequisites.concepts);
      }
      if (frontmatter.prerequisites.procedures) {
        deps.push(...frontmatter.prerequisites.procedures);
      }
    }
    
    return deps;
  }

  async loadMetadata() {
    try {
      const files = await fs.readdir(this.config.metadataDir);
      
      for (const file of files) {
        if (file.endsWith('.yaml') || file.endsWith('.yml')) {
          const content = await fs.readFile(
            path.join(this.config.metadataDir, file),
            'utf8'
          );
          const key = path.basename(file, path.extname(file));
          this.metadata[key] = yaml.load(content);
        }
      }
    } catch (error) {
      console.warn('Metadata directory not found');
    }
  }

  async loadAssemblies() {
    try {
      const files = await fs.readdir(this.config.assembliesDir);
      
      for (const file of files) {
        if (file.endsWith('.yaml') || file.endsWith('.yml')) {
          const content = await fs.readFile(
            path.join(this.config.assembliesDir, file),
            'utf8'
          );
          const assembly = yaml.load(content);
          const id = assembly.id || path.basename(file, path.extname(file));
          
          this.assemblies.set(id, assembly);
        }
      }
    } catch (error) {
      console.warn('Assemblies directory not found');
    }
    
    console.log(`📦 Loaded ${this.assemblies.size} assembly definitions`);
  }

  async assemble(assemblyId, options = {}) {
    const assembly = this.assemblies.get(assemblyId);
    if (!assembly) {
      throw new Error(`Assembly not found: ${assemblyId}`);
    }
    
    console.log(`🔨 Assembling: ${assembly.title || assemblyId}`);
    
    // Resolve modules based on criteria
    const modules = this.resolveModules(assembly, options);
    
    // Check prerequisites
    const { resolved, missing } = this.resolvePrerequisites(modules);
    
    if (missing.length > 0 && !options.ignorePrereqs) {
      console.warn(`⚠️  Missing prerequisites: ${missing.join(', ')}`);
    }
    
    // Generate output
    const output = await this.generateOutput(assembly, resolved, options);
    
    // Save output
    const outputPath = await this.saveOutput(assemblyId, output, options);
    
    console.log(`✅ Assembly complete: ${outputPath}`);
    
    return {
      path: outputPath,
      modules: resolved.length,
      missing: missing.length
    };
  }

  resolveModules(assembly, options) {
    const modules = [];
    
    // Get modules by explicit ID
    if (assembly.modules) {
      for (const moduleRef of assembly.modules) {
        const moduleId = typeof moduleRef === 'string' ? moduleRef : moduleRef.id;
        const module = this.modules.get(moduleId);
        
        if (module) {
          modules.push(module);
        } else {
          console.warn(`Module not found: ${moduleId}`);
        }
      }
    }
    
    // Get modules by criteria
    if (assembly.criteria) {
      for (const [moduleId, module] of this.modules) {
        if (this.matchesCriteria(module, assembly.criteria, options)) {
          modules.push(module);
        }
      }
    }
    
    // Apply filters
    return this.applyFilters(modules, assembly.filters || {}, options);
  }

  matchesCriteria(module, criteria, options) {
    // Check module type
    if (criteria.types && !criteria.types.includes(module.type)) {
      return false;
    }
    
    // Check tags
    if (criteria.tags) {
      const moduleTags = module.frontmatter.tags || [];
      const hasRequiredTags = criteria.tags.some(tag => moduleTags.includes(tag));
      if (!hasRequiredTags) {
        return false;
      }
    }
    
    // Check audience
    if (criteria.audience && options.audience) {
      const moduleAudience = module.frontmatter.audience || [];
      if (!moduleAudience.includes(options.audience)) {
        return false;
      }
    }
    
    // Check experience level
    if (criteria.level && options.level) {
      const moduleLevel = module.frontmatter.level;
      const levels = ['beginner', 'intermediate', 'advanced'];
      const requiredIndex = levels.indexOf(options.level);
      const moduleIndex = levels.indexOf(moduleLevel);
      
      if (moduleIndex > requiredIndex) {
        return false;
      }
    }
    
    return true;
  }

  applyFilters(modules, filters, options) {
    let filtered = [...modules];
    
    // Filter by deployment type
    if (filters.deployment && options.deployment) {
      filtered = filtered.filter(m => {
        const deployments = m.frontmatter.deployments || ['all'];
        return deployments.includes('all') || deployments.includes(options.deployment);
      });
    }
    
    // Filter by feature flags
    if (filters.features && options.features) {
      filtered = filtered.filter(m => {
        const required = m.frontmatter.requires_features || [];
        return required.every(f => options.features.includes(f));
      });
    }
    
    // Sort by priority
    if (filters.sort) {
      filtered.sort((a, b) => {
        const priorityA = a.frontmatter.priority || 999;
        const priorityB = b.frontmatter.priority || 999;
        return priorityA - priorityB;
      });
    }
    
    return filtered;
  }

  resolvePrerequisites(modules) {
    const resolved = [];
    const included = new Set();
    const missing = new Set();
    
    // Build dependency graph
    const visit = (module) => {
      if (included.has(module.id)) {
        return;
      }
      
      // Check dependencies
      for (const dep of module.dependencies) {
        const depModule = this.modules.get(dep);
        if (depModule) {
          visit(depModule);
        } else {
          missing.add(dep);
        }
      }
      
      included.add(module.id);
      resolved.push(module);
    };
    
    // Visit all modules
    for (const module of modules) {
      visit(module);
    }
    
    return {
      resolved,
      missing: Array.from(missing)
    };
  }

  async generateOutput(assembly, modules, options) {
    const format = options.format || assembly.format || 'markdown';
    
    switch (format) {
      case 'markdown':
        return this.generateMarkdown(assembly, modules, options);
      case 'html':
        return this.generateHTML(assembly, modules, options);
      case 'pdf':
        return this.generatePDF(assembly, modules, options);
      default:
        throw new Error(`Unsupported format: ${format}`);
    }
  }

  generateMarkdown(assembly, modules, options) {
    const sections = [];
    
    // Title and introduction
    sections.push(`# ${assembly.title || 'Documentation'}\n`);
    
    if (assembly.introduction) {
      sections.push(assembly.introduction + '\n');
    }
    
    // Table of contents
    sections.push('## Table of Contents\n');
    const toc = this.generateTOC(modules, assembly.structure);
    sections.push(toc + '\n');
    
    // Module content
    const structured = this.structureModules(modules, assembly.structure);
    
    for (const section of structured) {
      sections.push(`## ${section.title}\n`);
      
      if (section.introduction) {
        sections.push(section.introduction + '\n');
      }
      
      for (const module of section.modules) {
        // Add module content with adjusted heading levels
        const adjustedContent = this.adjustHeadingLevels(module.content, 2);
        sections.push(adjustedContent + '\n');
      }
    }
    
    // Appendices
    if (assembly.appendices) {
      sections.push('## Appendices\n');
      for (const appendix of assembly.appendices) {
        sections.push(`### ${appendix.title}\n`);
        sections.push(appendix.content + '\n');
      }
    }
    
    return sections.join('\n');
  }

  generateTOC(modules, structure) {
    const lines = [];
    const structured = this.structureModules(modules, structure);
    
    for (const section of structured) {
      lines.push(`- [${section.title}](#${this.slugify(section.title)})`);
      
      for (const module of section.modules) {
        const title = module.frontmatter.title || module.id;
        lines.push(`  - [${title}](#${this.slugify(title)})`);
      }
    }
    
    return lines.join('\n');
  }

  structureModules(modules, structure = {}) {
    if (!structure.sections) {
      // Default structure by module type
      return [
        {
          title: 'Concepts',
          modules: modules.filter(m => m.type === 'concepts')
        },
        {
          title: 'Tutorials',
          modules: modules.filter(m => m.type === 'tutorials')
        },
        {
          title: 'Procedures',
          modules: modules.filter(m => m.type === 'procedures')
        },
        {
          title: 'Reference',
          modules: modules.filter(m => m.type === 'reference')
        }
      ].filter(s => s.modules.length > 0);
    }
    
    // Custom structure
    const structured = [];
    const used = new Set();
    
    for (const section of structure.sections) {
      const sectionModules = [];
      
      for (const moduleRef of section.modules || []) {
        const module = modules.find(m => m.id === moduleRef);
        if (module && !used.has(module.id)) {
          sectionModules.push(module);
          used.add(module.id);
        }
      }
      
      if (sectionModules.length > 0) {
        structured.push({
          title: section.title,
          introduction: section.introduction,
          modules: sectionModules
        });
      }
    }
    
    // Add any unused modules to a misc section
    const unused = modules.filter(m => !used.has(m.id));
    if (unused.length > 0) {
      structured.push({
        title: 'Additional Topics',
        modules: unused
      });
    }
    
    return structured;
  }

  adjustHeadingLevels(content, baseLevel) {
    return content.replace(/^(#+)/gm, (match, hashes) => {
      const level = hashes.length + baseLevel - 1;
      return '#'.repeat(Math.min(level, 6));
    });
  }

  slugify(text) {
    return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  }

  async generateHTML(assembly, modules, options) {
    const markdown = this.generateMarkdown(assembly, modules, options);
    const html = marked.parse(markdown);
    
    // Wrap in HTML template
    const template = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${assembly.title || 'Documentation'}</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 24px;
            margin-bottom: 16px;
        }
        code {
            background: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
        }
        pre {
            background: #f4f4f4;
            padding: 16px;
            border-radius: 5px;
            overflow-x: auto;
        }
        blockquote {
            border-left: 4px solid #ddd;
            margin: 0;
            padding-left: 16px;
            color: #666;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 16px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background: #f4f4f4;
            font-weight: bold;
        }
        .toc {
            background: #f9f9f9;
            border: 1px solid #ddd;
            padding: 16px;
            margin-bottom: 32px;
            border-radius: 5px;
        }
        .toc ul {
            list-style: none;
            padding-left: 20px;
        }
        .toc > ul {
            padding-left: 0;
        }
    </style>
</head>
<body>
    ${html}
</body>
</html>
    `;
    
    return template;
  }

  async generatePDF(assembly, modules, options) {
    // Generate HTML first
    const html = await this.generateHTML(assembly, modules, options);
    
    // Use puppeteer or similar to convert to PDF
    // This is a placeholder - actual implementation would use puppeteer
    console.log('PDF generation requires puppeteer installation');
    return html;
  }

  async saveOutput(assemblyId, content, options) {
    const format = options.format || 'markdown';
    const extension = format === 'markdown' ? 'md' : format;
    const filename = `${assemblyId}.${extension}`;
    const outputPath = path.join(this.config.outputDir, filename);
    
    await fs.mkdir(this.config.outputDir, { recursive: true });
    await fs.writeFile(outputPath, content);
    
    return outputPath;
  }

  async validateModules() {
    const issues = [];
    
    for (const [id, module] of this.modules) {
      // Check required frontmatter
      const required = ['title', 'description', 'module_type'];
      for (const field of required) {
        if (!module.frontmatter[field]) {
          issues.push(`${id}: Missing required field '${field}'`);
        }
      }
      
      // Check dependencies exist
      for (const dep of module.dependencies) {
        if (!this.modules.has(dep)) {
          issues.push(`${id}: Unknown dependency '${dep}'`);
        }
      }
      
      // Check for circular dependencies
      const circular = this.findCircularDependencies(id);
      if (circular.length > 0) {
        issues.push(`${id}: Circular dependency detected: ${circular.join(' -> ')}`);
      }
    }
    
    return issues;
  }

  findCircularDependencies(startId) {
    const visited = new Set();
    const path = [];
    
    const visit = (id) => {
      if (path.includes(id)) {
        return [...path.slice(path.indexOf(id)), id];
      }
      
      if (visited.has(id)) {
        return null;
      }
      
      visited.add(id);
      path.push(id);
      
      const module = this.modules.get(id);
      if (module) {
        for (const dep of module.dependencies) {
          const circular = visit(dep);
          if (circular) {
            return circular;
          }
        }
      }
      
      path.pop();
      return null;
    };
    
    return visit(startId) || [];
  }

  async createModule(type, name, options = {}) {
    const templatePath = path.join(
      this.config.templatesDir || './templates',
      `${type}.md.template`
    );
    
    let template;
    try {
      template = await fs.readFile(templatePath, 'utf8');
    } catch (error) {
      throw new Error(`Template not found for type: ${type}`);
    }
    
    // Compile template
    const compiled = Handlebars.compile(template);
    
    // Generate content
    const moduleId = options.id || this.slugify(name);
    const content = compiled({
      MODULE_ID: moduleId,
      TITLE: name,
      DESCRIPTION: options.description || `${name} documentation`,
      TAG_1: options.tags?.[0] || 'untagged',
      TAG_2: options.tags?.[1] || 'draft',
      VERSION: '1.0.0',
      LAST_UPDATED: new Date().toISOString().split('T')[0],
      ...options.data
    });
    
    // Save module
    const dir = path.join(this.config.modulesDir, `${type}s`);
    await fs.mkdir(dir, { recursive: true });
    
    const filename = `${moduleId}.md`;
    const filepath = path.join(dir, filename);
    
    await fs.writeFile(filepath, content);
    
    console.log(`✅ Created module: ${filepath}`);
    return filepath;
  }
}

// CLI interface
if (require.main === module) {
  const program = require('commander');
  
  program
    .command('assemble <assembly>')
    .description('Assemble documentation from modules')
    .option('-f, --format <format>', 'Output format (markdown, html, pdf)', 'markdown')
    .option('-a, --audience <audience>', 'Target audience')
    .option('-l, --level <level>', 'Experience level')
    .option('-d, --deployment <type>', 'Deployment type')
    .option('--features <features>', 'Feature flags (comma-separated)')
    .option('--ignore-prereqs', 'Ignore missing prerequisites')
    .action(async (assembly, options) => {
      const assembler = new ModuleAssembler();
      await assembler.initialize();
      
      if (options.features) {
        options.features = options.features.split(',');
      }
      
      await assembler.assemble(assembly, options);
    });
  
  program
    .command('create <type> <name>')
    .description('Create a new documentation module')
    .option('-d, --description <desc>', 'Module description')
    .option('-t, --tags <tags>', 'Tags (comma-separated)')
    .action(async (type, name, options) => {
      const assembler = new ModuleAssembler();
      
      if (options.tags) {
        options.tags = options.tags.split(',');
      }
      
      await assembler.createModule(type, name, options);
    });
  
  program
    .command('validate')
    .description('Validate all documentation modules')
    .action(async () => {
      const assembler = new ModuleAssembler();
      await assembler.initialize();
      
      const issues = await assembler.validateModules();
      
      if (issues.length > 0) {
        console.log('⚠️  Validation issues found:');
        issues.forEach(issue => console.log(`  - ${issue}`));
        process.exit(1);
      } else {
        console.log('✅ All modules are valid');
      }
    });
  
  program
    .command('list')
    .description('List all modules')
    .option('-t, --type <type>', 'Filter by type')
    .action(async (options) => {
      const assembler = new ModuleAssembler();
      await assembler.initialize();
      
      const modules = Array.from(assembler.modules.values());
      const filtered = options.type 
        ? modules.filter(m => m.type === options.type)
        : modules;
      
      console.table(
        filtered.map(m => ({
          ID: m.id,
          Type: m.type,
          Title: m.frontmatter.title,
          Tags: (m.frontmatter.tags || []).join(', ')
        }))
      );
    });
  
  program.parse(process.argv);
}

module.exports = ModuleAssembler;
