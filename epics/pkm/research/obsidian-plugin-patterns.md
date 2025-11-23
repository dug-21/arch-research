# Obsidian Plugin Development Patterns for PKM Enhancement

## Executive Summary

This research report analyzes Obsidian plugin development patterns with a focus on building MCP-connected, AI-enhanced plugins for Personal Knowledge Management (PKM). Based on analysis of official documentation, popular plugins (Dataview, Templater, Smart Connections), and MCP integration patterns.

---

## 1. Plugin Architecture

### 1.1 Core Structure

Every Obsidian plugin consists of three essential files:

```
my-plugin/
  ├── main.js          # Compiled entry point (from TypeScript)
  ├── manifest.json    # Plugin metadata
  └── styles.css       # Optional styling
```

**manifest.json structure:**
```json
{
  "id": "my-plugin-id",
  "name": "My Plugin",
  "version": "1.0.0",
  "minAppVersion": "0.13.11",
  "description": "Plugin description",
  "author": "Author Name",
  "authorUrl": "https://example.com",
  "isDesktopOnly": false
}
```

### 1.2 Plugin Class

All plugins extend the `Plugin` base class:

```typescript
import { Plugin, App, PluginManifest } from 'obsidian';

export default class MyPlugin extends Plugin {
  settings: MyPluginSettings;

  async onload() {
    // Plugin initialization
    await this.loadSettings();

    // Register components
    this.addRibbonIcon('icon-name', 'Tooltip', () => {});
    this.addCommand({ id: 'command-id', name: 'Command Name', callback: () => {} });
    this.addSettingTab(new MySettingTab(this.app, this));
    this.registerView(VIEW_TYPE, (leaf) => new MyView(leaf));

    // Register events with automatic cleanup
    this.registerEvent(this.app.workspace.on('file-open', (file) => {}));
    this.registerDomEvent(document, 'click', (evt) => {});
    this.registerInterval(window.setInterval(() => {}, 5000));
  }

  async onunload() {
    // Cleanup resources
  }

  async loadSettings() {
    this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
  }

  async saveSettings() {
    await this.saveData(this.settings);
  }
}
```

### 1.3 Major API Modules

| Module | Purpose | Access |
|--------|---------|--------|
| **App** | Global application object | `this.app` |
| **Vault** | File and folder operations | `this.app.vault` |
| **Workspace** | Panes, views, UI management | `this.app.workspace` |
| **MetadataCache** | Cached file metadata | `this.app.metadataCache` |

---

## 2. Data Access

### 2.1 Vault API

The Vault API provides file system operations:

```typescript
// Core file types
type TAbstractFile = TFile | TFolder;

// Read files
const content = await this.app.vault.read(file);
const cachedRead = await this.app.vault.cachedRead(file);

// Write files
await this.app.vault.create('path/to/file.md', 'content');
await this.app.vault.modify(file, 'new content');
await this.app.vault.append(file, 'additional content');

// File operations
await this.app.vault.rename(file, 'new-path.md');
await this.app.vault.delete(file);
await this.app.vault.copy(file, 'destination.md');

// List files
const markdownFiles = this.app.vault.getMarkdownFiles();
const allFiles = this.app.vault.getAllLoadedFiles();

// Background modifications (preferred for non-active files)
await this.app.vault.process(file, (content) => {
  return content.replace('old', 'new');
});
```

### 2.2 MetadataCache API

Cached metadata for all markdown files:

```typescript
// Get cached metadata for a file
const cache = this.app.metadataCache.getFileCache(file);

// Available cached data
cache.frontmatter     // YAML frontmatter object
cache.headings        // Array of headings
cache.links           // Internal links
cache.embeds          // Embedded content
cache.tags            // Tags in content
cache.blocks          // Block references
cache.sections        // Document sections

// Position information for each item
interface Pos {
  start: { line: number; col: number; offset: number };
  end: { line: number; col: number; offset: number };
}

// Event: metadata cache updated
this.registerEvent(
  this.app.metadataCache.on('changed', (file, data, cache) => {
    // React to metadata changes
  })
);

// Resolve links
const linkedFile = this.app.metadataCache.getFirstLinkpathDest(
  linkpath,
  sourcePath
);
```

### 2.3 Frontmatter Handling

```typescript
// Read frontmatter from cache
const frontmatter = this.app.metadataCache.getFileCache(file)?.frontmatter;

// Parse with gray-matter (for full parsing)
import matter from 'gray-matter';

const content = await this.app.vault.read(file);
const { data, content: body } = matter(content);

// Update frontmatter
async function updateFrontmatter(file: TFile, updates: Record<string, any>) {
  await this.app.vault.process(file, (content) => {
    const parsed = matter(content);
    Object.assign(parsed.data, updates);
    return matter.stringify(parsed.content, parsed.data);
  });
}
```

### 2.4 Dataview Pattern: Data Indexing

Dataview's architecture demonstrates effective indexing:

```typescript
// Two data sources
// 1. Frontmatter (YAML)
---
title: My Note
tags: [research, ai]
created: 2024-01-15
---

// 2. Inline fields
Author:: John Doe
Status:: In Progress

// Query types
// - DQL (SQL-like query language)
// - Inline expressions
// - DataviewJS (full JavaScript API)
// - Inline JS expressions

// Security model
// - Regular queries: sandboxed, read-only
// - JavaScript queries: full plugin access (network, files)
```

---

## 3. UI Integration

### 3.1 Commands

```typescript
this.addCommand({
  id: 'unique-command-id',
  name: 'Human-Readable Command Name',
  icon: 'icon-name', // Lucide icon

  // Simple callback
  callback: () => {
    // Execute command
  },

  // Or with editor context
  editorCallback: (editor: Editor, view: MarkdownView) => {
    const selection = editor.getSelection();
    editor.replaceSelection('new text');
  },

  // Or check if command should be available
  checkCallback: (checking: boolean) => {
    const activeFile = this.app.workspace.getActiveFile();
    if (activeFile) {
      if (!checking) {
        // Execute command
      }
      return true;
    }
    return false;
  }
});
```

### 3.2 Settings Tab

```typescript
import { PluginSettingTab, Setting } from 'obsidian';

class MySettingTab extends PluginSettingTab {
  plugin: MyPlugin;

  constructor(app: App, plugin: MyPlugin) {
    super(app, plugin);
    this.plugin = plugin;
  }

  display(): void {
    const { containerEl } = this;
    containerEl.empty();

    // Section heading
    containerEl.createEl('h2', { text: 'Settings' });

    // Text setting
    new Setting(containerEl)
      .setName('API Key')
      .setDesc('Your API key for the service')
      .addText(text => text
        .setPlaceholder('Enter API key')
        .setValue(this.plugin.settings.apiKey)
        .onChange(async (value) => {
          this.plugin.settings.apiKey = value;
          await this.plugin.saveSettings();
        }));

    // Dropdown
    new Setting(containerEl)
      .setName('Model')
      .addDropdown(dropdown => dropdown
        .addOption('gpt-4', 'GPT-4')
        .addOption('claude-3', 'Claude 3')
        .setValue(this.plugin.settings.model)
        .onChange(async (value) => {
          this.plugin.settings.model = value;
          await this.plugin.saveSettings();
        }));

    // Toggle
    new Setting(containerEl)
      .setName('Enable feature')
      .addToggle(toggle => toggle
        .setValue(this.plugin.settings.enabled)
        .onChange(async (value) => {
          this.plugin.settings.enabled = value;
          await this.plugin.saveSettings();
        }));
  }
}
```

### 3.3 Modals

```typescript
import { Modal, App } from 'obsidian';

class MyModal extends Modal {
  result: string;
  onSubmit: (result: string) => void;

  constructor(app: App, onSubmit: (result: string) => void) {
    super(app);
    this.onSubmit = onSubmit;
  }

  onOpen() {
    const { contentEl } = this;

    contentEl.createEl('h2', { text: 'Enter your input' });

    const inputEl = contentEl.createEl('input', {
      type: 'text',
      placeholder: 'Type here...'
    });

    const submitBtn = contentEl.createEl('button', { text: 'Submit' });
    submitBtn.addEventListener('click', () => {
      this.onSubmit(inputEl.value);
      this.close();
    });
  }

  onClose() {
    const { contentEl } = this;
    contentEl.empty();
  }
}

// Usage
new MyModal(this.app, (result) => {
  console.log('User entered:', result);
}).open();
```

### 3.4 Custom Views

```typescript
import { ItemView, WorkspaceLeaf } from 'obsidian';

export const VIEW_TYPE_EXAMPLE = 'example-view';

class ExampleView extends ItemView {
  constructor(leaf: WorkspaceLeaf) {
    super(leaf);
  }

  getViewType(): string {
    return VIEW_TYPE_EXAMPLE;
  }

  getDisplayText(): string {
    return 'Example View';
  }

  getIcon(): string {
    return 'dice';
  }

  async onOpen() {
    const container = this.containerEl.children[1];
    container.empty();
    container.createEl('h4', { text: 'My Custom View' });

    // Build your UI here
  }

  async onClose() {
    // Cleanup
  }
}

// Register in plugin
this.registerView(
  VIEW_TYPE_EXAMPLE,
  (leaf) => new ExampleView(leaf)
);

// Activate the view
async activateView() {
  const { workspace } = this.app;

  let leaf = workspace.getLeavesOfType(VIEW_TYPE_EXAMPLE)[0];

  if (!leaf) {
    const rightLeaf = workspace.getRightLeaf(false);
    await rightLeaf.setViewState({
      type: VIEW_TYPE_EXAMPLE,
      active: true
    });
    leaf = rightLeaf;
  }

  workspace.revealLeaf(leaf);
}
```

### 3.5 Editor Extensions (CodeMirror 6)

```typescript
import { Extension } from '@codemirror/state';
import { ViewPlugin, DecorationSet } from '@codemirror/view';

// Register extension
const extension: Extension = ViewPlugin.fromClass(
  class {
    decorations: DecorationSet;

    constructor(view: EditorView) {
      this.decorations = this.buildDecorations(view);
    }

    update(update: ViewUpdate) {
      if (update.docChanged || update.viewportChanged) {
        this.decorations = this.buildDecorations(update.view);
      }
    }

    buildDecorations(view: EditorView): DecorationSet {
      // Return decorations
    }
  },
  { decorations: v => v.decorations }
);

// In plugin onload
this.registerEditorExtension(extension);

// Dynamic updates
const extensions: Extension[] = [];
this.registerEditorExtension(extensions);

// Later, modify and update
extensions.push(newExtension);
this.app.workspace.updateOptions();
```

### 3.6 Markdown Post Processor

```typescript
// For Reading view customization
this.registerMarkdownPostProcessor((element, context) => {
  const codeBlocks = element.querySelectorAll('code');

  codeBlocks.forEach(block => {
    if (block.textContent?.startsWith('%%')) {
      // Custom processing
      const replacement = document.createElement('div');
      replacement.addClass('my-custom-element');
      replacement.textContent = 'Processed content';
      block.replaceWith(replacement);
    }
  });
});

// Register code block processor
this.registerMarkdownCodeBlockProcessor('my-lang', (source, el, ctx) => {
  // Process code block with language 'my-lang'
  const result = processMyLanguage(source);
  el.createEl('div', { text: result });
});
```

---

## 4. External Connections

### 4.1 HTTP Requests with requestUrl

Obsidian provides `requestUrl()` to bypass CORS restrictions:

```typescript
import { requestUrl, RequestUrlParam, RequestUrlResponse } from 'obsidian';

// Basic GET request
const response = await requestUrl('https://api.example.com/data');
const data = response.json;

// POST with options
const response = await requestUrl({
  url: 'https://api.example.com/endpoint',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`
  },
  body: JSON.stringify({ prompt: 'Hello' })
});

// Handle streaming (workaround with Node fetch)
// Replace global fetch with node's fetch to eliminate CORS
const originalFetch = globalThis.fetch;
globalThis.fetch = require('node-fetch');

// Now packages like @anthropic-ai/sdk work correctly
const anthropic = new Anthropic({ apiKey });
const stream = await anthropic.messages.stream({
  model: 'claude-3-sonnet',
  messages: [{ role: 'user', content: 'Hello' }]
});
```

### 4.2 Multi-Provider AI Integration Pattern

Based on Smart Connections architecture:

```typescript
interface AIProvider {
  name: string;
  apiKey?: string;
  baseUrl?: string;
  model: string;
}

interface AIProviderConfig {
  openai?: AIProvider;
  anthropic?: AIProvider;
  ollama?: AIProvider;
  openrouter?: AIProvider;
}

class AIService {
  private config: AIProviderConfig;

  async chat(messages: Message[], provider: string): Promise<string> {
    switch (provider) {
      case 'openai':
        return this.chatOpenAI(messages);
      case 'anthropic':
        return this.chatAnthropic(messages);
      case 'ollama':
        return this.chatOllama(messages);
      default:
        throw new Error(`Unknown provider: ${provider}`);
    }
  }

  async generateEmbeddings(text: string): Promise<number[]> {
    // Local embedding with transformers.js
    // or API-based embedding
  }
}
```

### 4.3 WebSocket Connections

```typescript
class WebSocketManager {
  private ws: WebSocket;
  private reconnectAttempts = 0;

  connect(url: string) {
    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      this.reconnectAttempts = 0;
      console.log('Connected');
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleMessage(data);
    };

    this.ws.onclose = () => {
      this.reconnect(url);
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  private reconnect(url: string) {
    if (this.reconnectAttempts < 5) {
      setTimeout(() => {
        this.reconnectAttempts++;
        this.connect(url);
      }, 1000 * Math.pow(2, this.reconnectAttempts));
    }
  }

  send(data: any) {
    if (this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  disconnect() {
    this.ws?.close();
  }
}
```

---

## 5. Popular PKM Plugin Patterns

### 5.1 Dataview - Query Engine Pattern

**Architecture:**
- **FullIndex**: Central data indexing system
- **DataviewApi**: Query processing interface
- **Rendering System**: View-specific rendering logic

**Key Patterns:**
```typescript
// Plugin initialization
class DataviewPlugin extends Plugin {
  index: FullIndex;
  api: DataviewApi;

  async onload() {
    this.index = new FullIndex(this.app, this.settings);
    this.api = new DataviewApi(this.app, this.index);

    // Expose API globally for other plugins
    (window as any).DataviewAPI = this.api;

    // Register query processors
    this.registerMarkdownCodeBlockProcessor('dataview', ...);
    this.registerMarkdownCodeBlockProcessor('dataviewjs', ...);
  }
}

// Expose npm package for integration
// blacksmithgu/obsidian-dataview on NPM
```

### 5.2 Templater - Template Engine Pattern

**Architecture:**
- Template syntax parser
- JavaScript execution sandbox
- Module system for extensibility
- System command execution

**Key Patterns:**
```typescript
// Template syntax
<% tp.file.title %>
<% tp.date.now("YYYY-MM-DD") %>
<%*
  // JavaScript execution
  const response = await fetch('...');
  tR += await response.text();
%>

// User script integration
// scripts/myFunction.js
function myFunction(tp) {
  return tp.file.title.toUpperCase();
}
module.exports = myFunction;

// Usage: <% tp.user.myFunction() %>
```

### 5.3 Smart Connections - Semantic Search Pattern

**Architecture:**
- Multi-provider AI integration
- Local embedding generation
- Vector similarity search
- Conversational interface

**Key Patterns:**
```typescript
// Embedding generation
class EmbeddingService {
  async embed(text: string): Promise<number[]> {
    // Use local transformers.js or API
    return await this.model.embed(text);
  }

  cosineSimilarity(a: number[], b: number[]): number {
    // Calculate similarity
  }

  async findSimilar(query: string, notes: Note[]): Promise<ScoredNote[]> {
    const queryEmbedding = await this.embed(query);

    return notes
      .map(note => ({
        note,
        score: this.cosineSimilarity(queryEmbedding, note.embedding)
      }))
      .sort((a, b) => b.score - a.score);
  }
}
```

---

## 6. MCP Integration Patterns

### 6.1 MCP Server Architecture

Based on obsidian-mcp-tools:

```typescript
// Monorepo structure
mcp-project/
  ├── mcp-server/       # MCP server implementation
  ├── obsidian-plugin/  # Obsidian plugin UI
  └── shared/           # Common types and utilities

// MCP server acts as secure bridge
// Never grants direct file access to AI applications
// Mediates all interactions through API layer
```

### 6.2 Available MCP Tools

| Tool | Description | Dependencies |
|------|-------------|--------------|
| **Vault Access** | Read notes securely | Local REST API plugin |
| **Semantic Search** | Context-based searching | Smart Connections plugin |
| **Template Integration** | Execute templates | Templater plugin |

### 6.3 MCP Server Setup Pattern

```typescript
// Claude Desktop configuration (claude_desktop_config.json)
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["obsidian-mcp-server"],
      "env": {
        "OBSIDIAN_API_KEY": "your-api-key",
        "OBSIDIAN_HOST": "http://127.0.0.1",
        "OBSIDIAN_PORT": "27123"
      }
    }
  }
}

// Alternative with uvx
{
  "mcpServers": {
    "mcp-obsidian": {
      "command": "uvx",
      "args": ["mcp-obsidian"],
      "env": {
        "OBSIDIAN_API_KEY": "your-key",
        "OBSIDIAN_HOST": "http://localhost:27123"
      }
    }
  }
}
```

### 6.4 Building MCP Tools

```typescript
// Define MCP tool schema
const tools = {
  search_notes: {
    description: 'Search notes by semantic similarity',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Search query' },
        limit: { type: 'number', default: 10 }
      },
      required: ['query']
    },
    handler: async (input) => {
      const results = await semanticSearch(input.query, input.limit);
      return results;
    }
  },

  read_note: {
    description: 'Read a note by path',
    inputSchema: {
      type: 'object',
      properties: {
        path: { type: 'string', description: 'Note path' }
      },
      required: ['path']
    },
    handler: async (input) => {
      return await readNote(input.path);
    }
  },

  execute_template: {
    description: 'Execute a Templater template',
    inputSchema: {
      type: 'object',
      properties: {
        templatePath: { type: 'string' },
        parameters: { type: 'object' }
      },
      required: ['templatePath']
    },
    handler: async (input) => {
      return await executeTemplate(input.templatePath, input.parameters);
    }
  }
};
```

---

## 7. AI-Enhanced Plugin Patterns

### 7.1 Plugin with AI Chat Interface

```typescript
import { ItemView, WorkspaceLeaf } from 'obsidian';

class AIChatView extends ItemView {
  private messages: Message[] = [];
  private aiService: AIService;

  async onOpen() {
    const container = this.containerEl.children[1];
    container.addClass('ai-chat-container');

    // Chat history
    const historyEl = container.createDiv('chat-history');

    // Input area
    const inputArea = container.createDiv('input-area');
    const textArea = inputArea.createEl('textarea');
    const sendBtn = inputArea.createEl('button', { text: 'Send' });

    sendBtn.addEventListener('click', () => this.sendMessage(textArea.value));
  }

  async sendMessage(content: string) {
    // Add user message
    this.messages.push({ role: 'user', content });
    this.renderMessages();

    // Get context from current note
    const activeFile = this.app.workspace.getActiveFile();
    let context = '';
    if (activeFile) {
      context = await this.app.vault.read(activeFile);
    }

    // Enhance with semantic search
    const related = await this.findRelatedNotes(content);

    // Build system prompt with context
    const systemPrompt = `You are a PKM assistant. Current note context:
${context}

Related notes:
${related.map(n => n.content).join('\n\n')}`;

    // Get AI response
    const response = await this.aiService.chat([
      { role: 'system', content: systemPrompt },
      ...this.messages
    ]);

    this.messages.push({ role: 'assistant', content: response });
    this.renderMessages();
  }

  async findRelatedNotes(query: string): Promise<Note[]> {
    // Use embeddings for semantic search
    const embedding = await this.aiService.embed(query);
    // Find similar notes
    return this.searchByEmbedding(embedding);
  }
}
```

### 7.2 Automatic Linking with AI

```typescript
class AutoLinkPlugin extends Plugin {
  async onload() {
    this.registerEvent(
      this.app.vault.on('modify', async (file) => {
        if (file instanceof TFile && file.extension === 'md') {
          await this.suggestLinks(file);
        }
      })
    );
  }

  async suggestLinks(file: TFile) {
    const content = await this.app.vault.read(file);
    const allNotes = this.app.vault.getMarkdownFiles();

    // Get embeddings for content
    const contentEmbedding = await this.aiService.embed(content);

    // Find similar notes
    const similar = await Promise.all(
      allNotes
        .filter(n => n.path !== file.path)
        .map(async n => ({
          file: n,
          score: await this.similarity(contentEmbedding, n)
        }))
    );

    const suggestions = similar
      .filter(s => s.score > 0.7)
      .sort((a, b) => b.score - a.score)
      .slice(0, 5);

    if (suggestions.length > 0) {
      new LinkSuggestionModal(this.app, suggestions).open();
    }
  }
}
```

### 7.3 Smart Summarization

```typescript
this.addCommand({
  id: 'summarize-note',
  name: 'Summarize current note',
  editorCallback: async (editor, view) => {
    const content = editor.getValue();

    const summary = await this.aiService.chat([
      {
        role: 'system',
        content: 'Summarize the following note in 3-5 bullet points.'
      },
      {
        role: 'user',
        content: content
      }
    ]);

    // Add summary to frontmatter
    const file = view.file;
    await this.app.vault.process(file, (content) => {
      const parsed = matter(content);
      parsed.data.summary = summary;
      return matter.stringify(parsed.content, parsed.data);
    });

    new Notice('Summary added to frontmatter');
  }
});
```

### 7.4 RAG (Retrieval-Augmented Generation) Pattern

```typescript
class RAGService {
  private vectorStore: VectorStore;
  private aiService: AIService;

  async indexVault() {
    const files = this.app.vault.getMarkdownFiles();

    for (const file of files) {
      const content = await this.app.vault.read(file);
      const chunks = this.chunkContent(content);

      for (const chunk of chunks) {
        const embedding = await this.aiService.embed(chunk);
        await this.vectorStore.upsert({
          id: `${file.path}-${chunk.index}`,
          embedding,
          metadata: {
            path: file.path,
            content: chunk.text
          }
        });
      }
    }
  }

  async query(question: string): Promise<string> {
    // Get relevant chunks
    const queryEmbedding = await this.aiService.embed(question);
    const results = await this.vectorStore.search(queryEmbedding, 5);

    // Build context
    const context = results
      .map(r => `[${r.metadata.path}]\n${r.metadata.content}`)
      .join('\n\n---\n\n');

    // Generate answer
    return await this.aiService.chat([
      {
        role: 'system',
        content: `Answer based on the following context from the user's notes:

${context}

If the answer cannot be found in the context, say so.`
      },
      {
        role: 'user',
        content: question
      }
    ]);
  }

  private chunkContent(content: string): Chunk[] {
    // Split by headings or paragraphs
    // Overlap chunks for better context
    const chunks: Chunk[] = [];
    const paragraphs = content.split(/\n\n+/);

    let currentChunk = '';
    let index = 0;

    for (const para of paragraphs) {
      if (currentChunk.length + para.length > 1000) {
        chunks.push({ index: index++, text: currentChunk });
        currentChunk = para;
      } else {
        currentChunk += '\n\n' + para;
      }
    }

    if (currentChunk) {
      chunks.push({ index: index++, text: currentChunk });
    }

    return chunks;
  }
}
```

---

## 8. Best Practices & Security

### 8.1 Performance Optimization

**Lifecycle Management:**
```typescript
// Always use registerEvent for automatic cleanup
this.registerEvent(this.app.workspace.on('file-open', handler));

// Never store view references
// Let Obsidian manage view lifecycle

// Use debouncing for frequent operations
import { debounce } from 'obsidian';
const debouncedSave = debounce(this.saveSettings, 500, true);
```

**API Best Practices:**
- Use `Vault.process()` for background file modifications
- Use `normalizePath()` for user-provided paths
- Use `requestUrl()` instead of `fetch()`
- Use Platform API for OS detection
- Avoid `console.log` in production

**Startup Optimization:**
- Defer non-critical initialization
- Load large datasets lazily
- Cache computed results

### 8.2 Security Guidelines

**Code Safety:**
```typescript
// AVOID innerHTML/outerHTML (XSS risk)
element.innerHTML = userContent; // BAD

// USE safe DOM methods
element.createEl('div', { text: userContent }); // GOOD
element.textContent = userContent; // GOOD
```

**API Keys:**
```typescript
// Store in plugin settings (encrypted by Obsidian)
interface Settings {
  apiKey: string;
}

// Use password input type
new Setting(containerEl)
  .setName('API Key')
  .addText(text => text
    .inputEl.type = 'password');
```

**Community Plugin Requirements:**
- All plugins undergo initial review
- Must adhere to Obsidian Developer Policies
- Plugins inherit Obsidian's access levels
- Can access files, network, install programs
- Recommend independent security audits for sensitive data

### 8.3 Accessibility

```typescript
// Make interactive elements keyboard accessible
button.setAttribute('tabindex', '0');
button.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    button.click();
  }
});

// Provide ARIA labels for icon buttons
iconButton.setAttribute('aria-label', 'Search notes');

// Clear focus indicators
button.addClass('mod-cta'); // Obsidian's focus styles
```

### 8.4 UI/UX Guidelines

- Use sentence case for all UI text
- Avoid "command" in command names/IDs
- Don't include plugin ID in command IDs
- Don't set default hotkeys
- Use `.setHeading()` for settings headings
- Use Obsidian CSS variables for consistent theming

---

## 9. Development Workflow

### 9.1 Project Setup

```bash
# Clone sample plugin
git clone https://github.com/obsidianmd/obsidian-sample-plugin
cd obsidian-sample-plugin
npm install

# Development build with watch
npm run dev

# Production build
npm run build
```

### 9.2 Testing

```bash
# Copy to vault plugins folder
cp main.js styles.css manifest.json \
  /path/to/vault/.obsidian/plugins/my-plugin/

# Enable in Obsidian settings
# Hot reload: Cmd+R or Settings > Community Plugins > Reload
```

### 9.3 Publishing

1. Update `manifest.json` version
2. Update `versions.json` for compatibility
3. Create GitHub release with:
   - `main.js`
   - `manifest.json`
   - `styles.css` (if applicable)
4. Submit to community plugins

---

## 10. Resources

### Official
- [Obsidian API Repository](https://github.com/obsidianmd/obsidian-api)
- [Sample Plugin Template](https://github.com/obsidianmd/obsidian-sample-plugin)
- [Official Documentation](https://docs.obsidian.md/Plugins)

### Community
- [Unofficial Plugin Docs](https://marcusolsson.github.io/obsidian-plugin-docs/)
- [Obsidian Forum - Developers](https://forum.obsidian.md/c/developers/)
- [Obsidian Discord](https://discord.gg/obsidianmd)

### Reference Plugins
- [Dataview](https://github.com/blacksmithgu/obsidian-dataview) - Query engine
- [Templater](https://github.com/SilentVoid13/Templater) - Template engine
- [Smart Connections](https://github.com/brianpetro/obsidian-smart-connections) - AI integration
- [Obsidian MCP Tools](https://github.com/jacksteamdev/obsidian-mcp-tools) - MCP integration

### MCP Resources
- [mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian) - MCP server for Obsidian
- [obsidian-mcp-server](https://github.com/cyanheads/obsidian-mcp-server) - Comprehensive MCP server
- [MCP Specification](https://modelcontextprotocol.io/)

---

## Conclusion

Building MCP-connected, AI-enhanced Obsidian plugins requires understanding:

1. **Core Architecture**: Plugin lifecycle, major APIs (Vault, Workspace, MetadataCache)
2. **Data Access**: File operations, frontmatter, caching patterns
3. **UI Components**: Commands, settings, modals, views, editor extensions
4. **External Connections**: requestUrl for HTTP, WebSocket for real-time
5. **MCP Integration**: Server architecture, tool definitions, security
6. **AI Patterns**: Embeddings, semantic search, RAG, chat interfaces

The combination of Obsidian's rich plugin API and MCP's standardized AI connectivity opens powerful possibilities for PKM enhancement, from automatic linking and summarization to conversational interfaces that understand your entire knowledge base.
