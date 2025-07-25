#!/usr/bin/env node

/**
 * Mermaid Design System Documentation Generator
 * Automatically generates documentation from Mermaid diagrams
 */

const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process').promises;
const Handlebars = require('handlebars');
const matter = require('gray-matter');

class MermaidDocsGenerator {
  constructor(config = {}) {
    this.config = {
      sourceDir: config.sourceDir || './architecture',
      outputDir: config.outputDir || './generated',
      templateDir: config.templateDir || './templates',
      formats: config.formats || ['markdown', 'html', 'pdf'],
      ...config
    };
  }

  async generate() {
    console.log('🎨 Starting Mermaid documentation generation...');
    
    // Scan for .mmd files
    const mmdFiles = await this.scanForMermaidFiles();
    console.log(`📊 Found ${mmdFiles.length} Mermaid diagrams`);
    
    // Process each file
    for (const file of mmdFiles) {
      await this.processFile(file);
    }
    
    // Generate index
    await this.generateIndex(mmdFiles);
    
    console.log('✅ Documentation generation complete!');
  }

  async scanForMermaidFiles() {
    const files = [];
    
    async function scan(dir) {
      const entries = await fs.readdir(dir, { withFileTypes: true });
      
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        
        if (entry.isDirectory()) {
          await scan(fullPath);
        } else if (entry.name.endsWith('.mmd')) {
          files.push(fullPath);
        }
      }
    }
    
    await scan(this.config.sourceDir);
    return files;
  }

  async processFile(filePath) {
    console.log(`📄 Processing: ${path.basename(filePath)}`);
    
    // Read and parse file
    const content = await fs.readFile(filePath, 'utf8');
    const { data: metadata, content: diagram } = matter(content);
    
    // Extract diagram info
    const info = this.extractDiagramInfo(diagram);
    
    // Generate documentation for each format
    for (const format of this.config.formats) {
      await this.generateFormat(filePath, diagram, metadata, info, format);
    }
  }

  extractDiagramInfo(diagram) {
    const info = {
      type: 'unknown',
      title: '',
      description: '',
      components: [],
      relationships: []
    };
    
    // Detect diagram type
    if (diagram.includes('graph')) {
      info.type = 'graph';
    } else if (diagram.includes('sequenceDiagram')) {
      info.type = 'sequence';
    } else if (diagram.includes('classDiagram')) {
      info.type = 'class';
    }
    
    // Extract comments
    const commentRegex = /%%\s*(.+?)\s*$/gm;
    let match;
    while ((match = commentRegex.exec(diagram)) !== null) {
      const comment = match[1];
      if (comment.startsWith('Title:')) {
        info.title = comment.replace('Title:', '').trim();
      } else if (comment.startsWith('Description:')) {
        info.description = comment.replace('Description:', '').trim();
      }
    }
    
    return info;
  }

  async generateFormat(filePath, diagram, metadata, info, format) {
    const outputPath = this.getOutputPath(filePath, format);
    await fs.mkdir(path.dirname(outputPath), { recursive: true });
    
    switch (format) {
      case 'markdown':
        await this.generateMarkdown(outputPath, diagram, metadata, info);
        break;
      case 'html':
        await this.generateHTML(outputPath, diagram, metadata, info);
        break;
      case 'pdf':
        await this.generatePDF(outputPath, diagram, metadata, info);
        break;
    }
  }

  async generateMarkdown(outputPath, diagram, metadata, info) {
    const template = await this.loadTemplate('markdown.hbs');
    const compiled = Handlebars.compile(template);
    
    const content = compiled({
      ...metadata,
      ...info,
      diagram,
      timestamp: new Date().toISOString()
    });
    
    await fs.writeFile(outputPath, content);
  }

  async generateHTML(outputPath, diagram, metadata, info) {
    const template = await this.loadTemplate('html.hbs');
    const compiled = Handlebars.compile(template);
    
    const content = compiled({
      ...metadata,
      ...info,
      diagram,
      timestamp: new Date().toISOString(),
      mermaidCDN: 'https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js'
    });
    
    await fs.writeFile(outputPath, content);
  }

  async generatePDF(outputPath, diagram, metadata, info) {
    // First generate HTML
    const htmlPath = outputPath.replace('.pdf', '.html');
    await this.generateHTML(htmlPath, diagram, metadata, info);
    
    // Convert to PDF using puppeteer or similar
    await exec(`npx puppeteer-pdf ${htmlPath} ${outputPath}`);
  }

  async loadTemplate(name) {
    const templatePath = path.join(this.config.templateDir, name);
    return await fs.readFile(templatePath, 'utf8');
  }

  getOutputPath(inputPath, format) {
    const relative = path.relative(this.config.sourceDir, inputPath);
    const parsed = path.parse(relative);
    parsed.ext = `.${format}`;
    return path.join(this.config.outputDir, format, path.format(parsed));
  }

  async generateIndex(files) {
    console.log('📚 Generating documentation index...');
    
    const index = {
      title: 'Architecture Documentation',
      generated: new Date().toISOString(),
      diagrams: []
    };
    
    for (const file of files) {
      const content = await fs.readFile(file, 'utf8');
      const { data: metadata } = matter(content);
      const info = this.extractDiagramInfo(content);
      
      index.diagrams.push({
        path: path.relative(this.config.sourceDir, file),
        ...metadata,
        ...info
      });
    }
    
    // Generate index in each format
    for (const format of this.config.formats) {
      await this.generateIndexFormat(index, format);
    }
  }

  async generateIndexFormat(index, format) {
    const template = await this.loadTemplate(`index.${format}.hbs`);
    const compiled = Handlebars.compile(template);
    const content = compiled(index);
    
    const outputPath = path.join(this.config.outputDir, format, `index.${format}`);
    await fs.writeFile(outputPath, content);
  }
}

// CLI interface
if (require.main === module) {
  const generator = new MermaidDocsGenerator();
  generator.generate().catch(console.error);
}

module.exports = MermaidDocsGenerator;
