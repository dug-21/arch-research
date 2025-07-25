#!/usr/bin/env node

/**
 * ADR (Architecture Decision Record) Generator
 * Automates creation and management of ADRs
 */

const fs = require('fs').promises;
const path = require('path');
const inquirer = require('inquirer');
const { format } = require('date-fns');
const Handlebars = require('handlebars');
const yaml = require('js-yaml');

class ADRGenerator {
  constructor(config = {}) {
    this.config = {
      adrDir: config.adrDir || './architecture/decisions',
      templatePath: config.templatePath || './adr-template.md',
      indexPath: config.indexPath || './architecture/decisions/index.md',
      ...config
    };
  }

  async create(title, options = {}) {
    // Get next ADR number
    const number = await this.getNextNumber();
    const paddedNumber = String(number).padStart(4, '0');
    
    // Gather additional information
    const answers = await this.promptForDetails(title, options);
    
    // Generate ADR content
    const content = await this.generateContent({
      NUMBER: paddedNumber,
      TITLE: title,
      DATE: format(new Date(), 'yyyy-MM-dd'),
      STATUS: 'Proposed',
      ...answers,
      ...options
    });
    
    // Write ADR file
    const filename = `${paddedNumber}-${this.slugify(title)}.md`;
    const filepath = path.join(this.config.adrDir, filename);
    await fs.writeFile(filepath, content);
    
    // Update index
    await this.updateIndex(number, title, filename);
    
    console.log(`✅ Created ADR: ${filepath}`);
    return filepath;
  }

  async getNextNumber() {
    try {
      const files = await fs.readdir(this.config.adrDir);
      const numbers = files
        .filter(f => f.match(/^\d{4}-/))
        .map(f => parseInt(f.substring(0, 4)))
        .filter(n => !isNaN(n));
      
      return numbers.length > 0 ? Math.max(...numbers) + 1 : 1;
    } catch (error) {
      // Directory doesn't exist yet
      await fs.mkdir(this.config.adrDir, { recursive: true });
      return 1;
    }
  }

  async promptForDetails(title, options) {
    if (options.batch) {
      return this.generateDefaults();
    }
    
    const questions = [
      {
        type: 'input',
        name: 'CONTEXT_DESCRIPTION',
        message: 'Describe the context:',
        default: 'We need to make a decision about...'
      },
      {
        type: 'input',
        name: 'PROBLEM_STATEMENT',
        message: 'What is the problem?',
        default: 'The current approach...'
      },
      {
        type: 'input',
        name: 'DECISION_STATEMENT',
        message: 'What is the decision?',
        default: 'We will...'
      },
      {
        type: 'input',
        name: 'AUTHOR',
        message: 'Author name:',
        default: options.author || process.env.USER
      }
    ];
    
    return await inquirer.prompt(questions);
  }

  generateDefaults() {
    return {
      CONTEXT_DESCRIPTION: 'Context description pending...',
      PROBLEM_STATEMENT: 'Problem statement pending...',
      DECISION_STATEMENT: 'Decision pending...',
      CONSTRAINT_1: 'TBD',
      CONSTRAINT_2: 'TBD',
      CONSTRAINT_3: 'TBD',
      OPTION_1_NAME: 'Option 1',
      OPTION_1_DESC: 'Description pending...',
      OPTION_1_PRO_1: 'TBD',
      OPTION_1_PRO_2: 'TBD',
      OPTION_1_CON_1: 'TBD',
      OPTION_1_CON_2: 'TBD',
      OPTION_2_NAME: 'Option 2',
      OPTION_2_DESC: 'Description pending...',
      OPTION_2_PRO_1: 'TBD',
      OPTION_2_PRO_2: 'TBD',
      OPTION_2_CON_1: 'TBD',
      OPTION_2_CON_2: 'TBD',
      OPTION_3_NAME: 'Selected Option',
      OPTION_3_DESC: 'Description pending...',
      OPTION_3_PRO_1: 'TBD',
      OPTION_3_PRO_2: 'TBD',
      OPTION_3_CON_1: 'TBD',
      OPTION_3_CON_2: 'TBD',
      POSITIVE_CONSEQUENCE_1: 'TBD',
      POSITIVE_CONSEQUENCE_2: 'TBD',
      POSITIVE_CONSEQUENCE_3: 'TBD',
      NEGATIVE_CONSEQUENCE_1: 'TBD',
      NEGATIVE_CONSEQUENCE_2: 'TBD',
      NEUTRAL_CONSEQUENCE_1: 'TBD',
      NEUTRAL_CONSEQUENCE_2: 'TBD',
      STEP_1: 'TBD',
      STEP_2: 'TBD',
      STEP_3: 'TBD',
      VALIDATION_CRITERIA_1: 'TBD',
      VALIDATION_CRITERIA_2: 'TBD',
      VALIDATION_CRITERIA_3: 'TBD',
      REFERENCE_1: 'TBD',
      REFERENCE_2: 'TBD',
      RELATED_ADRS: 'None',
      AUTHOR: process.env.USER || 'Unknown',
      REVIEWERS: 'TBD'
    };
  }

  async generateContent(data) {
    const template = await fs.readFile(this.config.templatePath, 'utf8');
    const compiled = Handlebars.compile(template);
    return compiled(data);
  }

  slugify(text) {
    return text
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
  }

  async updateIndex(number, title, filename) {
    let indexContent = '# Architecture Decision Records\n\n';
    
    try {
      indexContent = await fs.readFile(this.config.indexPath, 'utf8');
    } catch (error) {
      // Index doesn't exist yet
    }
    
    // Add new entry
    const entry = `\n- [ADR-${String(number).padStart(4, '0')}: ${title}](./${filename})`;
    
    // Insert in numerical order
    const lines = indexContent.split('\n');
    let inserted = false;
    
    for (let i = 0; i < lines.length; i++) {
      const match = lines[i].match(/ADR-(\d{4})/);
      if (match && parseInt(match[1]) > number) {
        lines.splice(i, 0, entry.trim());
        inserted = true;
        break;
      }
    }
    
    if (!inserted) {
      lines.push(entry.trim());
    }
    
    await fs.writeFile(this.config.indexPath, lines.join('\n'));
  }

  async list() {
    const files = await fs.readdir(this.config.adrDir);
    const adrs = [];
    
    for (const file of files) {
      if (file.match(/^\d{4}-.*\.md$/)) {
        const content = await fs.readFile(path.join(this.config.adrDir, file), 'utf8');
        const statusMatch = content.match(/## Status\n(.+)/);
        const titleMatch = content.match(/# ADR-\d{4}: (.+)/);
        
        adrs.push({
          file,
          number: parseInt(file.substring(0, 4)),
          title: titleMatch ? titleMatch[1] : 'Unknown',
          status: statusMatch ? statusMatch[1].trim() : 'Unknown'
        });
      }
    }
    
    return adrs.sort((a, b) => a.number - b.number);
  }

  async supersede(oldNumber, newTitle) {
    // Create new ADR
    const newPath = await this.create(newTitle, {
      batch: true,
      RELATED_ADRS: `ADR-${String(oldNumber).padStart(4, '0')}`
    });
    
    // Update old ADR status
    const files = await fs.readdir(this.config.adrDir);
    const oldFile = files.find(f => f.startsWith(String(oldNumber).padStart(4, '0')));
    
    if (oldFile) {
      const oldPath = path.join(this.config.adrDir, oldFile);
      let content = await fs.readFile(oldPath, 'utf8');
      content = content.replace(
        /## Status\n.+/,
        `## Status\nSuperseded by ${path.basename(newPath)}`
      );
      await fs.writeFile(oldPath, content);
    }
    
    return newPath;
  }

  async validate() {
    const adrs = await this.list();
    const issues = [];
    
    for (const adr of adrs) {
      const content = await fs.readFile(
        path.join(this.config.adrDir, adr.file),
        'utf8'
      );
      
      // Check for incomplete sections
      if (content.includes('TBD') || content.includes('pending')) {
        issues.push(`${adr.file}: Contains incomplete sections`);
      }
      
      // Check for missing required sections
      const requiredSections = ['Status', 'Context', 'Decision', 'Consequences'];
      for (const section of requiredSections) {
        if (!content.includes(`## ${section}`)) {
          issues.push(`${adr.file}: Missing required section: ${section}`);
        }
      }
    }
    
    return issues;
  }
}

// CLI interface
if (require.main === module) {
  const program = require('commander');
  const generator = new ADRGenerator();
  
  program
    .command('create <title>')
    .description('Create a new ADR')
    .option('-a, --author <name>', 'Author name')
    .option('-b, --batch', 'Skip interactive prompts')
    .action(async (title, options) => {
      await generator.create(title, options);
    });
  
  program
    .command('list')
    .description('List all ADRs')
    .action(async () => {
      const adrs = await generator.list();
      console.table(adrs);
    });
  
  program
    .command('supersede <oldNumber> <newTitle>')
    .description('Supersede an existing ADR')
    .action(async (oldNumber, newTitle) => {
      await generator.supersede(oldNumber, newTitle);
    });
  
  program
    .command('validate')
    .description('Validate all ADRs')
    .action(async () => {
      const issues = await generator.validate();
      if (issues.length > 0) {
        console.log('⚠️  Validation issues found:');
        issues.forEach(issue => console.log(`  - ${issue}`));
        process.exit(1);
      } else {
        console.log('✅ All ADRs are valid');
      }
    });
  
  program.parse(process.argv);
}

module.exports = ADRGenerator;
