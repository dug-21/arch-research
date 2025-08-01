# Practical Implementation Examples for Complex View Management

## 1. Interactive Filtering System Implementation

### JavaScript/D3.js Example

```javascript
class ArchitectureViewManager {
  constructor(data, container) {
    this.data = data;
    this.container = container;
    this.filters = {
      technology: [],
      domain: [],
      criticality: [],
      team: []
    };
    this.zoomLevel = 1;
    this.selectedLevel = 'overview';
  }

  // Multi-dimensional filtering
  applyFilters() {
    const filteredData = this.data.filter(node => {
      // AND logic for different dimensions
      const techMatch = this.filters.technology.length === 0 || 
                       this.filters.technology.includes(node.technology);
      const domainMatch = this.filters.domain.length === 0 || 
                         this.filters.domain.includes(node.domain);
      const criticalityMatch = this.filters.criticality.length === 0 || 
                              this.filters.criticality.includes(node.criticality);
      const teamMatch = this.filters.team.length === 0 || 
                       this.filters.team.includes(node.team);
      
      return techMatch && domainMatch && criticalityMatch && teamMatch;
    });
    
    this.updateView(filteredData);
  }

  // Semantic zoom implementation
  handleZoom(event) {
    this.zoomLevel = event.transform.k;
    
    // Change representation based on zoom level
    this.container.selectAll('.node')
      .each(function(d) {
        const node = d3.select(this);
        
        if (this.zoomLevel < 0.5) {
          // Overview: Icons only
          node.select('.details').style('display', 'none');
          node.select('.icon').style('display', 'block');
        } else if (this.zoomLevel < 1.5) {
          // Intermediate: Basic info
          node.select('.details').style('display', 'block');
          node.select('.full-details').style('display', 'none');
        } else {
          // Detailed: Everything
          node.select('.full-details').style('display', 'block');
        }
      });
  }

  // Progressive disclosure navigation
  drillDown(nodeId) {
    const node = this.data.find(n => n.id === nodeId);
    
    if (node.children) {
      // Save navigation context
      this.navigationStack.push({
        level: this.selectedLevel,
        nodeId: nodeId,
        filters: {...this.filters}
      });
      
      // Load child level
      this.selectedLevel = node.childLevel;
      this.data = node.children;
      this.render();
    }
  }
}
```

## 2. Color Coding System with Accessibility

### CSS Implementation

```css
/* Base color system with CSS variables */
:root {
  /* Technology colors */
  --color-database: #2E86AB;
  --color-application: #A23B72;
  --color-integration: #F18F01;
  --color-external: #C73E1D;
  --color-infrastructure: #6C757D;
  
  /* Status colors */
  --color-operational: #28A745;
  --color-warning: #FFC107;
  --color-critical: #DC3545;
  --color-planned: #007BFF;
  --color-deprecated: #6C757D;
  
  /* Accessibility patterns */
  --pattern-database: url("data:image/svg+xml,%3Csvg width='40' height='40'...");
  --pattern-application: url("data:image/svg+xml,%3Csvg width='40' height='40'...");
}

/* Color-blind friendly mode */
.colorblind-mode {
  --color-operational: #1E88E5;
  --color-warning: #FB8C00;
  --color-critical: #7B1FA2;
}

/* Component styling with patterns */
.architecture-node {
  fill: var(--color-database);
  stroke: #333;
  stroke-width: 2px;
}

.architecture-node.database {
  fill: var(--color-database);
  fill-opacity: 0.8;
}

/* High contrast mode */
@media (prefers-contrast: high) {
  .architecture-node {
    stroke-width: 3px;
    stroke: #000;
  }
}

/* Pattern overlay for accessibility */
.pattern-overlay {
  fill: var(--pattern-database);
  opacity: 0.3;
}
```

## 3. Dynamic View Generation with React

### React Component Example

```jsx
import React, { useState, useEffect, useMemo } from 'react';
import { Zoom } from '@visx/zoom';
import { Group } from '@visx/group';

const DynamicArchitectureView = ({ data, viewType }) => {
  const [filters, setFilters] = useState({});
  const [zoomLevel, setZoomLevel] = useState(1);
  const [selectedNodes, setSelectedNodes] = useState([]);

  // Memoized filtered data
  const filteredData = useMemo(() => {
    return applyFilters(data, filters, viewType);
  }, [data, filters, viewType]);

  // Dynamic layout based on view type
  const layout = useMemo(() => {
    switch(viewType) {
      case 'hierarchical':
        return calculateHierarchicalLayout(filteredData);
      case 'force':
        return calculateForceLayout(filteredData);
      case 'matrix':
        return calculateMatrixLayout(filteredData);
      default:
        return calculateDefaultLayout(filteredData);
    }
  }, [filteredData, viewType]);

  // Progressive rendering for performance
  const visibleNodes = useMemo(() => {
    const maxNodes = getMaxNodesForZoom(zoomLevel);
    return prioritizeNodes(layout.nodes, maxNodes, selectedNodes);
  }, [layout, zoomLevel, selectedNodes]);

  return (
    <div className="architecture-view">
      <ViewControls 
        filters={filters}
        onFilterChange={setFilters}
        viewType={viewType}
      />
      
      <Zoom
        width={width}
        height={height}
        scaleMin={0.1}
        scaleMax={10}
        onZoom={setZoomLevel}
      >
        {zoom => (
          <svg width={width} height={height}>
            <Group transform={zoom.toString()}>
              {visibleNodes.map(node => (
                <ArchitectureNode
                  key={node.id}
                  node={node}
                  zoomLevel={zoomLevel}
                  isSelected={selectedNodes.includes(node.id)}
                  onClick={() => handleNodeClick(node)}
                />
              ))}
              {renderConnections(visibleNodes, zoomLevel)}
            </Group>
          </svg>
        )}
      </Zoom>
      
      <MiniMap 
        data={layout}
        viewport={zoom.transformMatrix}
      />
    </div>
  );
};
```

## 4. Layered View Configuration

### JSON Configuration Example

```json
{
  "viewLayers": {
    "executive": {
      "name": "Executive Dashboard",
      "maxElements": 10,
      "abstractions": ["business-capability", "cost-center"],
      "metrics": ["roi", "risk", "budget"],
      "layout": "radial",
      "defaultFilters": {
        "importance": ["critical", "high"],
        "visibility": "executive"
      }
    },
    "architect": {
      "name": "Solution Architecture",
      "maxElements": 100,
      "abstractions": ["application", "service", "database"],
      "metrics": ["performance", "availability", "coupling"],
      "layout": "hierarchical",
      "defaultFilters": {
        "technical": true,
        "detail": "medium"
      }
    },
    "developer": {
      "name": "Development View",
      "maxElements": null,
      "abstractions": ["component", "api", "repository"],
      "metrics": ["coverage", "complexity", "dependencies"],
      "layout": "force-directed",
      "defaultFilters": {
        "technical": true,
        "detail": "high"
      }
    }
  },
  "transitionRules": {
    "executive-to-architect": {
      "trigger": "drill-down",
      "animation": "zoom-fade",
      "contextPreserve": ["selected-domain", "filters"]
    },
    "architect-to-developer": {
      "trigger": "component-click",
      "animation": "slide-expand",
      "contextPreserve": ["component-path", "related-services"]
    }
  }
}
```

## 5. Performance Optimization for Large Datasets

### WebGL-based Rendering Example

```javascript
class WebGLArchitectureRenderer {
  constructor(canvas, data) {
    this.gl = canvas.getContext('webgl2');
    this.data = data;
    this.visibleRange = { min: 0, max: 1000 };
    this.lodLevels = [
      { distance: 0, detail: 'full' },
      { distance: 100, detail: 'simplified' },
      { distance: 500, detail: 'icon' },
      { distance: 1000, detail: 'dot' }
    ];
  }

  // Frustum culling for performance
  cullInvisibleNodes(nodes, camera) {
    const frustum = this.calculateFrustum(camera);
    return nodes.filter(node => {
      const bounds = this.getNodeBounds(node);
      return this.frustumContains(frustum, bounds);
    });
  }

  // Level of detail (LOD) system
  selectLOD(node, camera) {
    const distance = this.calculateDistance(node.position, camera.position);
    
    for (let i = this.lodLevels.length - 1; i >= 0; i--) {
      if (distance >= this.lodLevels[i].distance) {
        return this.lodLevels[i].detail;
      }
    }
    return 'full';
  }

  // Instanced rendering for repeated elements
  renderInstanced(nodeType, instances) {
    const vertexBuffer = this.createVertexBuffer(nodeType);
    const instanceBuffer = this.createInstanceBuffer(instances);
    
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, vertexBuffer);
    this.gl.bindBuffer(this.gl.ARRAY_BUFFER, instanceBuffer);
    
    // Use instanced drawing
    this.gl.drawArraysInstanced(
      this.gl.TRIANGLES,
      0,
      vertexCount,
      instances.length
    );
  }

  // Spatial indexing for quick lookups
  buildSpatialIndex() {
    this.quadTree = new QuadTree({
      x: 0,
      y: 0,
      width: this.bounds.width,
      height: this.bounds.height
    });
    
    this.data.forEach(node => {
      this.quadTree.insert({
        x: node.x,
        y: node.y,
        width: node.width,
        height: node.height,
        data: node
      });
    });
  }
}
```

## 6. Real-time Dashboard Integration

### WebSocket-based Live Updates

```javascript
class LiveArchitectureDashboard {
  constructor(config) {
    this.config = config;
    this.nodes = new Map();
    this.metrics = new Map();
    this.ws = null;
  }

  connect() {
    this.ws = new WebSocket(this.config.wsEndpoint);
    
    this.ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      this.handleUpdate(update);
    };
  }

  handleUpdate(update) {
    switch(update.type) {
      case 'metric':
        this.updateMetric(update.nodeId, update.metric, update.value);
        break;
      case 'status':
        this.updateNodeStatus(update.nodeId, update.status);
        break;
      case 'topology':
        this.updateTopology(update.changes);
        break;
    }
  }

  updateMetric(nodeId, metric, value) {
    // Update metric with animation
    const node = this.nodes.get(nodeId);
    if (node) {
      // Smooth transition
      const oldValue = this.metrics.get(`${nodeId}-${metric}`) || 0;
      this.animateValue(node, metric, oldValue, value);
      
      // Update color based on threshold
      if (metric === 'cpu' && value > 80) {
        this.highlightNode(node, 'warning');
      }
    }
  }

  // Efficient diff-based updates
  updateTopology(changes) {
    changes.added?.forEach(node => {
      this.addNode(node, true); // animate = true
    });
    
    changes.removed?.forEach(nodeId => {
      this.removeNode(nodeId, true);
    });
    
    changes.modified?.forEach(change => {
      this.modifyNode(change.nodeId, change.properties);
    });
  }
}
```

## 7. Search and Navigation System

### Elasticsearch Integration Example

```javascript
class ArchitectureSearchEngine {
  constructor(esClient) {
    this.client = esClient;
    this.searchHistory = [];
  }

  async search(query, filters = {}) {
    const searchBody = {
      query: {
        bool: {
          must: [
            {
              multi_match: {
                query: query,
                fields: ['name^3', 'description', 'tags^2', 'team'],
                fuzziness: 'AUTO'
              }
            }
          ],
          filter: this.buildFilters(filters)
        }
      },
      highlight: {
        fields: {
          name: {},
          description: {}
        }
      },
      aggs: {
        by_type: {
          terms: { field: 'type' }
        },
        by_domain: {
          terms: { field: 'domain' }
        }
      }
    };

    const response = await this.client.search({
      index: 'architecture-components',
      body: searchBody
    });

    return this.processSearchResults(response);
  }

  // Intelligent query suggestions
  async getSuggestions(partial) {
    const suggestions = await this.client.search({
      index: 'architecture-components',
      body: {
        suggest: {
          component_suggest: {
            prefix: partial,
            completion: {
              field: 'name.suggest',
              fuzzy: {
                fuzziness: 2
              }
            }
          }
        }
      }
    });

    return suggestions.suggest.component_suggest[0].options;
  }

  // Context-aware navigation
  findPath(sourceId, targetId) {
    // Use graph traversal to find connection path
    const graph = this.buildGraph();
    return this.dijkstra(graph, sourceId, targetId);
  }
}
```

## 8. Export and Sharing Capabilities

### Multi-format Export System

```javascript
class ArchitectureExporter {
  constructor(viewManager) {
    this.viewManager = viewManager;
  }

  // SVG export with interactivity preserved
  exportSVG(options = {}) {
    const svg = this.viewManager.getSVGElement();
    const clone = svg.cloneNode(true);
    
    // Add CSS styles inline
    this.inlineStyles(clone);
    
    // Add interactive elements
    if (options.interactive) {
      this.addClickHandlers(clone);
    }
    
    // Add metadata
    this.addMetadata(clone, {
      created: new Date().toISOString(),
      version: this.viewManager.version,
      filters: this.viewManager.filters
    });
    
    return new Blob([clone.outerHTML], { type: 'image/svg+xml' });
  }

  // High-resolution PNG export
  async exportPNG(scale = 2) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    const bounds = this.viewManager.getBounds();
    canvas.width = bounds.width * scale;
    canvas.height = bounds.height * scale;
    
    ctx.scale(scale, scale);
    
    // Render at high resolution
    await this.viewManager.renderToCanvas(ctx);
    
    return new Promise(resolve => {
      canvas.toBlob(resolve, 'image/png');
    });
  }

  // Generate interactive HTML package
  exportInteractiveHTML() {
    const template = `
<!DOCTYPE html>
<html>
<head>
  <title>Architecture View - ${this.viewManager.title}</title>
  <style>${this.getEmbeddedStyles()}</style>
</head>
<body>
  <div id="architecture-container"></div>
  <script>
    const data = ${JSON.stringify(this.viewManager.getData())};
    const config = ${JSON.stringify(this.viewManager.getConfig())};
    ${this.getEmbeddedScript()}
  </script>
</body>
</html>
    `;
    
    return new Blob([template], { type: 'text/html' });
  }
}
```

This implementation guide provides practical, production-ready code examples for implementing complex architectural view management systems. The examples cover filtering, zooming, performance optimization, real-time updates, and export capabilities.