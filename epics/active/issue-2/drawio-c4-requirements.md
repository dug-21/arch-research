# Draw.io C4 Diagram Requirements

## Overview

This document outlines specific requirements and best practices for creating C4 architecture diagrams using Draw.io (diagrams.net).

## Draw.io Setup for C4 Diagrams

### 1. Installing C4 Shape Libraries

#### Method 1: Import XML Library
```
1. Download c4-draw.io-library.xml from GitHub
2. In Draw.io: File → Open Library from → Device
3. Select the downloaded XML file
4. C4 shapes will appear in the left sidebar
```

#### Method 2: Use GitHub Integration
```
1. File → Open Library from → URL
2. Enter: https://raw.githubusercontent.com/kaminzo/c4-draw.io/master/c4.drawio.library.xml
3. Click "Open"
```

### 2. Essential Draw.io Features for C4

#### Shape Data (Metadata)
- Select any shape and press `Cmd+M` (Mac) or `Ctrl+M` (Windows)
- Add properties:
  - `type`: Person, Software System, Container, Component
  - `technology`: Programming language, framework, database type
  - `description`: Brief explanation of purpose
  - `url`: Link to detailed documentation

#### Layers Management
- Use layers to organize complex diagrams:
  - Layer 1: Background and boundaries
  - Layer 2: Main elements (systems, containers)
  - Layer 3: Relationships and connections
  - Layer 4: Labels and annotations

#### Container Boundaries
- Use the "Container" shape from General shapes
- Set to transparent with dashed border
- Label clearly (e.g., "Web Application Boundary")

## C4 Element Specifications in Draw.io

### 1. Person Element
```
Shape: Rectangle with rounded corners or person icon
Color: #08427B (dark blue) or custom
Border: 2px solid
Font: Bold, 14pt
Content:
  - Name (bold)
  - [Person] tag
  - Description (italic)
```

### 2. Software System Element
```
Shape: Rectangle
Color: 
  - External: #999999 (grey)
  - Internal: #1168BD (blue)
Border: 2px solid
Font: Bold, 14pt
Content:
  - System Name (bold)
  - [Software System] tag
  - Description
```

### 3. Container Element
```
Shape: Rectangle
Color: #438DD5 (lighter blue)
Border: 2px solid
Font: Bold, 12pt
Content:
  - Container Name (bold)
  - [Container: Technology] tag
  - Description
  - Technology stack
```

### 4. Component Element
```
Shape: Rectangle
Color: #85BBF0 (light blue)
Border: 2px solid
Font: Regular, 11pt
Content:
  - Component Name (bold)
  - [Component] tag
  - Responsibility description
  - Technology details
```

### 5. Relationship Lines
```
Style: Solid line with arrow
Width: 2px
Color: #707070 (grey)
Label:
  - Action verb (e.g., "Uses", "Reads from")
  - Protocol/Technology [HTTPS/JSON]
  - Data flow description
```

## Draw.io Diagram Templates

### Context Diagram Template
```xml
<mxGraphModel>
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
    <!-- System Boundary -->
    <mxCell value="System Boundary" style="rounded=1;dashed=1;dashPattern=1 4" vertex="1" parent="1">
      <mxGeometry x="200" y="200" width="400" height="300" as="geometry"/>
    </mxCell>
    <!-- Add elements here -->
  </root>
</mxGraphModel>
```

### Container Diagram Structure
- Use swimlanes for logical grouping
- Group by:
  - Deployment environment (Web, Mobile, Cloud)
  - Architectural layer (Presentation, Business, Data)
  - Technology stack

### Component Diagram Organization
- Use nested containers for grouping
- Show component interfaces
- Include internal/external dependencies
- Use consistent spacing (grid: 20px)

## Draw.io Best Practices

### 1. Consistent Styling
Create and save custom styles:
```
Edit → Edit Style → Save as Default Style
```

Define styles for:
- C4Person
- C4SystemInternal
- C4SystemExternal
- C4Container
- C4Component
- C4Relationship

### 2. Layout Guidelines

#### Alignment
- Use Draw.io's alignment tools (Arrange menu)
- Maintain consistent spacing: 40-60px between elements
- Center-align text within shapes

#### Flow Direction
- Top to bottom for hierarchical views
- Left to right for process flows
- External systems on the edges

### 3. Navigation and Linking

#### Page Management
```
Right-click canvas → Insert Page
Name pages clearly:
- "1. System Context"
- "2. Container - Web App"
- "3. Components - API"
```

#### Creating Links
1. Select shape
2. Right-click → Edit Link
3. Choose "Link to Page" for internal navigation
4. Add external URLs for documentation

### 4. Export Settings

#### For Documentation
```
File → Export As → PNG
Settings:
- Border: 20px
- Shadow: Enabled
- Grid: Disabled
- Transparent Background: No
- Include Copy of Diagram: Yes
```

#### For Version Control
```
File → Export As → XML
- Compressed: Yes
- All Pages: Yes
```

## Draw.io Keyboard Shortcuts for C4

| Action | Windows/Linux | Mac |
|--------|--------------|-----|
| Edit Shape Data | Ctrl+M | Cmd+M |
| Duplicate | Ctrl+D | Cmd+D |
| Group Elements | Ctrl+G | Cmd+G |
| Align Left | Ctrl+Shift+L | Cmd+Shift+L |
| Distribute Horizontally | Ctrl+Shift+H | Cmd+Shift+H |
| Format Panel | Ctrl+Shift+P | Cmd+Shift+P |

## Advanced Draw.io Features

### 1. Custom Libraries
Create project-specific libraries:
```
File → New Library → Add shapes → Export
Share via URL or file
```

### 2. Placeholders and Variables
Use placeholders for reusable content:
```
%date% - Current date
%page% - Page number
%pagetitle% - Current page title
```

### 3. Smart Templates
Create smart templates with:
- Pre-defined styles
- Placeholder text
- Connection points
- Metadata fields

### 4. Collaboration Features
- Real-time collaboration (Draw.io online)
- Comments and annotations
- Revision history
- Export to Confluence/GitHub

## Quality Checklist for Draw.io C4 Diagrams

### Visual Quality
- [ ] Consistent colors per element type
- [ ] Readable fonts (min 10pt)
- [ ] No overlapping elements
- [ ] Clear relationship lines
- [ ] Proper alignment and spacing

### Content Quality
- [ ] All elements have complete information
- [ ] Technologies are specified
- [ ] Relationships are labeled
- [ ] Diagram has title and metadata
- [ ] Legend/key is included

### Technical Quality
- [ ] Links between pages work
- [ ] Exports include diagram data
- [ ] File names follow convention
- [ ] Version controlled
- [ ] Accessible color contrast

## Troubleshooting Common Issues

### Issue: Shapes not showing C4 styling
**Solution**: Ensure C4 library is loaded and shapes are from that library

### Issue: Text overflow in shapes
**Solution**: 
- Adjust shape size
- Use word wrap (Format → Text → Word Wrap)
- Reduce font size

### Issue: Diagram too complex
**Solution**:
- Split into multiple pages
- Use layers to show/hide details
- Create overview and detailed versions

### Issue: Lost custom styles
**Solution**:
- Save styles to library
- Export style configuration
- Use templates

## Resources and References

- Draw.io Documentation: https://www.diagrams.net/doc/
- C4 Model Official Site: https://c4model.com/
- Draw.io C4 Library: https://github.com/kaminzo/c4-draw.io
- Draw.io Templates: https://github.com/vadagama/c4-model-drawio-template