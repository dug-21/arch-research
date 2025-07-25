#!/usr/bin/env node

/**
 * Docs-as-Data Query Engine
 * Enables querying and analyzing documentation as structured data
 */

const fs = require('fs').promises;
const path = require('path');
const yaml = require('js-yaml');
const { graphql, buildSchema } = require('graphql');
const Ajv = require('ajv');
const glob = require('glob-promise');

class DocsQueryEngine {
  constructor(config = {}) {
    this.config = {
      dataDir: config.dataDir || './data',
      schemaDir: config.schemaDir || './data/schemas',
      outputDir: config.outputDir || './outputs',
      ...config
    };
    
    this.data = {
      components: [],
      flows: [],
      architecture: {}
    };
    
    this.validators = {};
  }

  async initialize() {
    // Load schemas
    await this.loadSchemas();
    
    // Load data
    await this.loadData();
    
    // Build GraphQL schema
    this.buildGraphQLSchema();
  }

  async loadSchemas() {
    const ajv = new Ajv({ allErrors: true });
    const schemaFiles = await glob(`${this.config.schemaDir}/*.schema.json`);
    
    for (const file of schemaFiles) {
      const schema = JSON.parse(await fs.readFile(file, 'utf8'));
      const type = path.basename(file, '.schema.json');
      this.validators[type] = ajv.compile(schema);
    }
  }

  async loadData() {
    // Load components
    const componentFiles = await glob(`${this.config.dataDir}/components/*.yaml`);
    for (const file of componentFiles) {
      const data = yaml.load(await fs.readFile(file, 'utf8'));
      if (this.validate('component', data)) {
        this.data.components.push(data);
      }
    }
    
    // Load flows
    const flowFiles = await glob(`${this.config.dataDir}/flows/*.json`);
    for (const file of flowFiles) {
      const data = JSON.parse(await fs.readFile(file, 'utf8'));
      if (this.validate('flow', data)) {
        this.data.flows.push(data);
      }
    }
    
    // Load architecture
    const archFiles = await glob(`${this.config.dataDir}/architecture/*.yaml`);
    for (const file of archFiles) {
      const data = yaml.load(await fs.readFile(file, 'utf8'));
      const key = path.basename(file, '.yaml');
      this.data.architecture[key] = data;
    }
  }

  validate(type, data) {
    if (!this.validators[type]) {
      console.warn(`No validator for type: ${type}`);
      return true;
    }
    
    const valid = this.validators[type](data);
    if (!valid) {
      console.error(`Validation failed for ${type}:`, this.validators[type].errors);
      return false;
    }
    
    return true;
  }

  buildGraphQLSchema() {
    const schemaDefinition = `
      type Component {
        id: String!
        name: String!
        type: String!
        description: String!
        owner: Owner!
        version: String!
        dependencies: Dependencies
        api: API
        infrastructure: Infrastructure
        quality: Quality
        security: Security
        tags: [String]
      }
      
      type Owner {
        team: String!
        contact: String!
        slack: String
      }
      
      type Dependencies {
        internal: [InternalDependency]
        external: [ExternalDependency]
      }
      
      type InternalDependency {
        id: String!
        version: String
        type: String!
        critical: Boolean
      }
      
      type ExternalDependency {
        name: String!
        version: String!
        license: String
        purpose: String
      }
      
      type API {
        type: String!
        specification: String
        endpoints: [Endpoint]
      }
      
      type Endpoint {
        method: String!
        path: String!
        description: String
        authentication: Boolean
      }
      
      type Infrastructure {
        runtime: String
        resources: Resources
        scaling: Scaling
      }
      
      type Resources {
        cpu: String
        memory: String
        storage: String
      }
      
      type Scaling {
        min: Int
        max: Int
        metric: String
      }
      
      type Quality {
        sla: SLA
        testing: Testing
      }
      
      type SLA {
        availability: String
        latency: Latency
      }
      
      type Latency {
        p50: String
        p95: String
        p99: String
      }
      
      type Testing {
        unit: Float
        integration: Float
        e2e: Float
      }
      
      type Security {
        classification: String
        authentication: [String]
        compliance: [String]
      }
      
      type Flow {
        id: String!
        name: String!
        description: String
        steps: [FlowStep]
      }
      
      type FlowStep {
        order: Int!
        component: String!
        action: String!
        next: [String]
      }
      
      type DependencyGraph {
        nodes: [Component]
        edges: [DependencyEdge]
      }
      
      type DependencyEdge {
        from: String!
        to: String!
        type: String!
      }
      
      type SecurityAudit {
        component: Component!
        issues: [SecurityIssue]
        score: Float!
      }
      
      type SecurityIssue {
        severity: String!
        description: String!
        recommendation: String!
      }
      
      type Query {
        # Component queries
        components(type: String, team: String, tag: String): [Component]
        component(id: String!): Component
        
        # Dependency queries
        dependencies(componentId: String!): DependencyGraph
        dependents(componentId: String!): [Component]
        criticalPath(from: String!, to: String!): [Component]
        
        # Flow queries
        flows: [Flow]
        flow(id: String!): Flow
        componentsInFlow(flowId: String!): [Component]
        
        # Analysis queries
        securityAudit(componentId: String): [SecurityAudit]
        performanceBottlenecks(threshold: Float): [Component]
        testCoverage(minimum: Float): [Component]
        externalDependencies(license: String): [ExternalDependency]
        
        # Architecture queries
        impactAnalysis(componentId: String!): [Component]
        singlePointsOfFailure: [Component]
      }
    `;
    
    this.schema = buildSchema(schemaDefinition);
    
    // Define resolvers
    this.rootValue = {
      components: (args) => this.queryComponents(args),
      component: (args) => this.getComponent(args.id),
      dependencies: (args) => this.getDependencyGraph(args.componentId),
      dependents: (args) => this.getDependents(args.componentId),
      criticalPath: (args) => this.getCriticalPath(args.from, args.to),
      flows: () => this.data.flows,
      flow: (args) => this.data.flows.find(f => f.id === args.id),
      componentsInFlow: (args) => this.getComponentsInFlow(args.flowId),
      securityAudit: (args) => this.performSecurityAudit(args.componentId),
      performanceBottlenecks: (args) => this.findPerformanceBottlenecks(args.threshold),
      testCoverage: (args) => this.checkTestCoverage(args.minimum),
      externalDependencies: (args) => this.getExternalDependencies(args.license),
      impactAnalysis: (args) => this.analyzeImpact(args.componentId),
      singlePointsOfFailure: () => this.findSinglePointsOfFailure()
    };
  }

  async query(queryString) {
    const result = await graphql({
      schema: this.schema,
      source: queryString,
      rootValue: this.rootValue
    });
    
    return result;
  }

  // Query implementations
  queryComponents({ type, team, tag }) {
    let results = this.data.components;
    
    if (type) {
      results = results.filter(c => c.type === type);
    }
    
    if (team) {
      results = results.filter(c => c.owner.team === team);
    }
    
    if (tag) {
      results = results.filter(c => c.tags && c.tags.includes(tag));
    }
    
    return results;
  }

  getComponent(id) {
    return this.data.components.find(c => c.id === id);
  }

  getDependencyGraph(componentId) {
    const component = this.getComponent(componentId);
    if (!component) return null;
    
    const nodes = [component];
    const edges = [];
    const visited = new Set([componentId]);
    
    // BFS to find all dependencies
    const queue = [component];
    
    while (queue.length > 0) {
      const current = queue.shift();
      
      if (current.dependencies && current.dependencies.internal) {
        for (const dep of current.dependencies.internal) {
          edges.push({
            from: current.id,
            to: dep.id,
            type: dep.type
          });
          
          if (!visited.has(dep.id)) {
            visited.add(dep.id);
            const depComponent = this.getComponent(dep.id);
            if (depComponent) {
              nodes.push(depComponent);
              queue.push(depComponent);
            }
          }
        }
      }
    }
    
    return { nodes, edges };
  }

  getDependents(componentId) {
    const dependents = [];
    
    for (const component of this.data.components) {
      if (component.dependencies && component.dependencies.internal) {
        const depends = component.dependencies.internal.some(d => d.id === componentId);
        if (depends) {
          dependents.push(component);
        }
      }
    }
    
    return dependents;
  }

  getCriticalPath(from, to) {
    // Implement Dijkstra's or similar to find critical path
    // This is a simplified version
    const path = [];
    const visited = new Set();
    
    const findPath = (current, target, currentPath) => {
      if (current === target) {
        return currentPath;
      }
      
      visited.add(current);
      const component = this.getComponent(current);
      
      if (component && component.dependencies && component.dependencies.internal) {
        for (const dep of component.dependencies.internal) {
          if (!visited.has(dep.id)) {
            const result = findPath(dep.id, target, [...currentPath, this.getComponent(dep.id)]);
            if (result) return result;
          }
        }
      }
      
      return null;
    };
    
    return findPath(from, to, [this.getComponent(from)]) || [];
  }

  getComponentsInFlow(flowId) {
    const flow = this.data.flows.find(f => f.id === flowId);
    if (!flow) return [];
    
    const componentIds = new Set();
    for (const step of flow.steps) {
      componentIds.add(step.component);
    }
    
    return Array.from(componentIds).map(id => this.getComponent(id)).filter(Boolean);
  }

  performSecurityAudit(componentId) {
    const components = componentId 
      ? [this.getComponent(componentId)].filter(Boolean)
      : this.data.components;
    
    return components.map(component => {
      const issues = [];
      let score = 100;
      
      // Check for security classification
      if (!component.security || !component.security.classification) {
        issues.push({
          severity: 'high',
          description: 'No security classification defined',
          recommendation: 'Define security classification (public, internal, confidential, restricted)'
        });
        score -= 20;
      }
      
      // Check authentication
      if (component.type === 'service' || component.type === 'api-gateway') {
        if (!component.security || !component.security.authentication || component.security.authentication.length === 0) {
          issues.push({
            severity: 'high',
            description: 'No authentication method defined',
            recommendation: 'Implement authentication (oauth2, jwt, api-key, mtls)'
          });
          score -= 30;
        }
      }
      
      // Check for known vulnerable dependencies
      if (component.dependencies && component.dependencies.external) {
        const vulnerableDeps = component.dependencies.external.filter(dep => {
          // Simplified check - in reality would check against vulnerability DB
          return dep.version && dep.version.includes('beta') || dep.version.includes('alpha');
        });
        
        if (vulnerableDeps.length > 0) {
          issues.push({
            severity: 'medium',
            description: `${vulnerableDeps.length} dependencies using pre-release versions`,
            recommendation: 'Update to stable versions'
          });
          score -= 10 * vulnerableDeps.length;
        }
      }
      
      return {
        component,
        issues,
        score: Math.max(0, score)
      };
    });
  }

  findPerformanceBottlenecks(threshold = 100) {
    return this.data.components.filter(component => {
      if (!component.quality || !component.quality.sla || !component.quality.sla.latency) {
        return false;
      }
      
      const p99 = parseInt(component.quality.sla.latency.p99);
      return p99 > threshold;
    });
  }

  checkTestCoverage(minimum = 80) {
    return this.data.components.filter(component => {
      if (!component.quality || !component.quality.testing) {
        return true; // Include components without testing info
      }
      
      const testing = component.quality.testing;
      return testing.unit < minimum || testing.integration < minimum;
    });
  }

  getExternalDependencies(license) {
    const dependencies = [];
    
    for (const component of this.data.components) {
      if (component.dependencies && component.dependencies.external) {
        for (const dep of component.dependencies.external) {
          if (!license || dep.license === license) {
            dependencies.push({
              ...dep,
              usedBy: component.id
            });
          }
        }
      }
    }
    
    return dependencies;
  }

  analyzeImpact(componentId) {
    const impacted = new Set();
    const queue = [componentId];
    
    while (queue.length > 0) {
      const current = queue.shift();
      const dependents = this.getDependents(current);
      
      for (const dependent of dependents) {
        if (!impacted.has(dependent.id)) {
          impacted.add(dependent.id);
          queue.push(dependent.id);
        }
      }
    }
    
    return Array.from(impacted).map(id => this.getComponent(id)).filter(Boolean);
  }

  findSinglePointsOfFailure() {
    const criticalComponents = [];
    
    for (const component of this.data.components) {
      const dependents = this.getDependents(component.id);
      
      // If more than 3 components depend on this one and it has no redundancy
      if (dependents.length > 3 && (!component.infrastructure || !component.infrastructure.scaling || component.infrastructure.scaling.min < 2)) {
        criticalComponents.push(component);
      }
    }
    
    return criticalComponents;
  }

  // Export functionality
  async exportResults(results, format = 'json') {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `query-results-${timestamp}.${format}`;
    const filepath = path.join(this.config.outputDir, 'reports', filename);
    
    await fs.mkdir(path.dirname(filepath), { recursive: true });
    
    switch (format) {
      case 'json':
        await fs.writeFile(filepath, JSON.stringify(results, null, 2));
        break;
      case 'yaml':
        await fs.writeFile(filepath, yaml.dump(results));
        break;
      case 'csv':
        // Implement CSV export
        break;
    }
    
    return filepath;
  }
}

// CLI interface
if (require.main === module) {
  const program = require('commander');
  
  program
    .command('query <query>')
    .description('Execute a GraphQL query against documentation')
    .option('-o, --output <format>', 'Output format (json, yaml, csv)', 'json')
    .action(async (queryString, options) => {
      const engine = new DocsQueryEngine();
      await engine.initialize();
      
      const result = await engine.query(queryString);
      
      if (result.errors) {
        console.error('Query errors:', result.errors);
        process.exit(1);
      }
      
      console.log(JSON.stringify(result.data, null, 2));
      
      if (options.output) {
        const filepath = await engine.exportResults(result.data, options.output);
        console.log(`Results exported to: ${filepath}`);
      }
    });
  
  program
    .command('validate')
    .description('Validate all documentation data against schemas')
    .action(async () => {
      const engine = new DocsQueryEngine();
      await engine.initialize();
      console.log('✅ All documentation data is valid');
    });
  
  program
    .command('analyze')
    .description('Run comprehensive analysis')
    .action(async () => {
      const engine = new DocsQueryEngine();
      await engine.initialize();
      
      console.log('🔍 Running comprehensive analysis...\n');
      
      // Security audit
      const securityAudit = await engine.performSecurityAudit();
      const insecure = securityAudit.filter(a => a.score < 80);
      console.log(`🔐 Security: ${insecure.length} components need attention`);
      
      // Performance
      const bottlenecks = await engine.findPerformanceBottlenecks();
      console.log(`⏱️  Performance: ${bottlenecks.length} potential bottlenecks`);
      
      // Test coverage
      const lowCoverage = await engine.checkTestCoverage();
      console.log(`🧪 Test Coverage: ${lowCoverage.length} components below threshold`);
      
      // Single points of failure
      const spof = await engine.findSinglePointsOfFailure();
      console.log(`⚠️  Reliability: ${spof.length} single points of failure`);
    });
  
  program.parse(process.argv);
}

module.exports = DocsQueryEngine;
