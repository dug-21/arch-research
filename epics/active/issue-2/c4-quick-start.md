# C4 Model Quick Start Guide

## What is C4?

The C4 model uses 4 levels of diagram to describe software architecture:
1. **Context** - The big picture
2. **Container** - High-level technology choices  
3. **Component** - What's inside each container
4. **Code** - How components are implemented (optional)

## Quick Setup in Draw.io

### Step 1: Get the C4 Shapes
1. Download the C4 shape library: [c4-draw.io](https://github.com/kaminzo/c4-draw.io)
2. In Draw.io: `File → Open Library from → Device`
3. Select the downloaded XML file

### Step 2: Start with Context
Create your first Context diagram:
- Add your system in the center
- Add users (Person shapes) 
- Add external systems
- Draw relationships with labeled arrows

## The Essential Elements

### 🧑 Person
```
Name: Customer
Type: [Person]
Description: Uses the system to...
```

### 📦 Software System
```
Name: E-Commerce Platform
Type: [Software System]
Description: Allows customers to...
```

### 🏗️ Container
```
Name: Web Application
Type: [Container: React]
Description: Delivers the UI to...
Technology: React, TypeScript
```

### 🔧 Component
```
Name: Shopping Cart Service
Type: [Component]
Description: Manages cart state...
Technology: TypeScript class
```

## The 5-Minute Context Diagram

1. **Create a new diagram**
   - Title: "System Context for [Your System]"
   
2. **Add the main system** (center)
   - Blue rectangle
   - Label with system name and description

3. **Add users** (top)
   - Person shapes
   - Different user types

4. **Add external systems** (around edges)
   - Grey rectangles
   - Systems your system depends on

5. **Connect with arrows**
   - User → System: "Uses"
   - System → External: "Sends data to"

## Best Practices Checklist

✅ **Every diagram needs:**
- [ ] A clear title
- [ ] A key/legend
- [ ] Element types in brackets [Container]
- [ ] Technology choices listed
- [ ] Labeled relationship arrows

❌ **Avoid these mistakes:**
- Too many elements (keep it under 15)
- Unlabeled arrows
- Missing element types
- No technology information
- Mixing abstraction levels

## Example Diagram Structure

### Level 1: Context
```
Who uses it? → [Your System] → What does it connect to?
```

### Level 2: Container  
```
[Web App] → [API] → [Database]
     ↓         ↓          ↓
   React    Spring    PostgreSQL
```

### Level 3: Component
```
[Controller] → [Service] → [Repository]
      ↓            ↓            ↓
   REST API   Business    Data Access
```

## Draw.io Pro Tips

### Organize with Pages
- Page 1: Context
- Page 2: Containers
- Page 3+: Components per container

### Use These Shortcuts
- `Cmd/Ctrl + M`: Edit shape data
- `Cmd/Ctrl + D`: Duplicate
- `Cmd/Ctrl + G`: Group elements

### Link Between Levels
1. Select a shape
2. Right-click → "Edit Link"
3. Link to the detailed diagram page

## Common Patterns

### Web Application
```
[Browser] → [Web App] → [API] → [Database]
           (React)    (REST)   (PostgreSQL)
```

### Microservices
```
[Gateway] → [Service A] → [Message Queue]
          → [Service B] → [Cache]
          → [Service C] → [Database]
```

### Mobile App
```
[Mobile App] → [API Gateway] → [Backend Services]
(iOS/Android)    (REST/GraphQL)
```

## Next Steps

1. **Start Simple**: Create a Context diagram first
2. **Get Feedback**: Show it to your team
3. **Add Detail**: Create Container diagrams for complex areas
4. **Keep Updated**: Refresh when architecture changes

## Helpful Resources

- 🎯 [C4 Model Website](https://c4model.com/)
- 📘 [Draw.io C4 Templates](https://github.com/vadagama/c4-model-drawio-template)
- 🎥 [C4 Model Video Tutorial](https://www.youtube.com/c4model)

---

Remember: The goal is clear communication, not perfect diagrams!