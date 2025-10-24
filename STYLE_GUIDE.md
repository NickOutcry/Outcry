# Outcry Application Style Guide

## Typography

### Font Families

#### Navigation Bar
- **Font**: Futura Light
- **Usage**: Navigation links, menu items
- **Weight**: 300 (Light)
- **Active State**: Underlined with bold line in hex color #f5b7a4

#### Headings
- **Font**: Gilroy Bold
- **Usage**: All headings (h1, h2, h3, h4, h5, h6)
- **Weight**: 700 (Bold)
- **Color**: #333 (Primary text color)

#### Body Text
- **Font**: Futura Medium
- **Usage**: Paragraphs, spans, divs, table cells, list items
- **Weight**: 500 (Medium)
- **Color**: #333 (Primary text color)

### Font Stack Fallbacks
```css
--font-futura-light: 'Futura Light', 'Futura', 'Arial', sans-serif;
--font-futura-medium: 'Futura Medium', 'Futura', 'Arial', sans-serif;
--font-gilroy-bold: 'Gilroy Bold', 'Gilroy', 'Inter', sans-serif;
```

## Color Palette

### Primary Colors
- **Accent Color**: #f5b7a4 (Peach/Coral)
- **Primary Text**: #333 (Dark Gray)
- **Secondary Text**: #666 (Medium Gray)
- **Background**: #ffffff (White)
- **Border**: #e0e0e0 (Light Gray)

### Usage
- **Accent Color (#f5b7a4)**: Active navigation underlines, selected tab indicators
- **Primary Text (#333)**: Main content, headings, active states
- **Secondary Text (#666)**: Inactive navigation, secondary information
- **Background (#ffffff)**: Page backgrounds, card backgrounds
- **Border (#e0e0e0)**: Subtle borders, dividers

## Navigation

### Active Page Indicator
- **Style**: Bold underline
- **Color**: #f5b7a4 (Accent color)
- **Position**: Below navigation link
- **Height**: 3px
- **Border Radius**: 2px

### Hover States
- **Background**: rgba(0, 0, 0, 0.1)
- **Transform**: translateY(-2px)
- **Transition**: 0.3s ease

## Table Tabs

### Layout
- **Position**: Left sidebar
- **Width**: 250px
- **Background**: White
- **Border**: Right border in #e0e0e0

### Tab Buttons
- **Font**: Futura Light
- **Weight**: 300 (Light)
- **Padding**: 1rem 1.5rem
- **Border Radius**: 8px
- **Transition**: 0.3s ease

### Selected Tab
- **Background**: rgba(245, 183, 164, 0.15)
- **Color**: #333 (Primary text)
- **Weight**: 400 (Medium)
- **Indicator**: Left border in #f5b7a4, 4px width

### Hover States
- **Background**: rgba(245, 183, 164, 0.1)
- **Color**: #333 (Primary text)

## Responsive Design

### Mobile Breakpoints
- **Tablet**: 768px and below
- **Mobile**: 480px and below

### Mobile Adaptations
- **Navigation**: Stack vertically
- **Table Tabs**: Move to top, full width
- **Typography**: Scale down appropriately
- **Spacing**: Reduce padding and margins

## CSS Variables

### Usage
All colors and fonts are defined as CSS custom properties for consistency:

```css
:root {
    --font-futura-light: 'Futura Light', 'Futura', 'Arial', sans-serif;
    --font-futura-medium: 'Futura Medium', 'Futura', 'Arial', sans-serif;
    --font-gilroy-bold: 'Gilroy Bold', 'Gilroy', 'Inter', sans-serif;
    --color-accent: #f5b7a4;
    --color-text-primary: #333;
    --color-text-secondary: #666;
    --color-background: #ffffff;
    --color-border: #e0e0e0;
}
```

## Implementation Examples

### Navigation Link
```html
<a href="/page" class="nav-link active">Page Name</a>
```

### Table Tabs
```html
<div class="tabs-container">
    <div class="tabs-sidebar">
        <ul class="tabs-menu">
            <li><button class="tab-button active">Tab 1</button></li>
            <li><button class="tab-button">Tab 2</button></li>
        </ul>
    </div>
    <div class="tab-content">
        <div class="tab-panel active">Content 1</div>
        <div class="tab-panel">Content 2</div>
    </div>
</div>
```

### Heading
```html
<h1 class="section-title">Page Title</h1>
```

## Accessibility

### Color Contrast
- All text meets WCAG AA standards for contrast
- Accent color used sparingly for emphasis only
- Hover states provide clear visual feedback

### Typography
- Font sizes scale appropriately for different screen sizes
- Line heights provide adequate spacing for readability
- Font weights provide clear hierarchy

### Interactive Elements
- All buttons and links have hover states
- Focus states are clearly visible
- Transitions are smooth and not jarring

