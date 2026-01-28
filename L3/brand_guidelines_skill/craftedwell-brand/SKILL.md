---
name: craftedwell-brand
description: CraftedWell brand guidelines for presentations and documents. Use this skill whenever creating or styling documents (docx, pdf) or presentations (pptx) for CraftedWell. Apply warm, artisanal aesthetic with chocolate/caramel color palette, Georgia headings, and Arial body text.
---

# CraftedWell Brand Guidelines

Apply CraftedWell's warm, artisanal brand to documents and presentations.

## Quick Reference

**Colors:**
- Primary text: Dark Chocolate `#3D2314`
- Headings: Chocolate `#5A2C10`
- Secondary: Cocoa `#8B4A24`
- Highlights: Caramel `#C07F43`, Soft Gold `#D4A45A`
- Backgrounds: Cream `#FDF8F3`, White `#FFFFFF`
- Borders: `#E5D5C5`

**Typography:**
- Headings: Georgia Bold
- Body: Arial

**Logos:** See `assets/` — use `logo-primary.png` on light backgrounds, `logo-reversed.png` on Dark Chocolate backgrounds only.

For complete specifications, read [`references/brand-guide.md`](references/brand-guide.md).

---

## Document Creation (docx)

Use with the `docx` skill. Apply these styles:

```javascript
// CraftedWell document styles for docx-js
const BRAND = {
  colors: {
    darkChocolate: "3D2314",
    chocolate: "5A2C10",
    cocoa: "8B4A24",
    caramel: "C07F43",
    cream: "FDF8F3",
    border: "E5D5C5"
  }
};

// Heading styles
paragraphStyles: [
  { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
    run: { size: 36, bold: true, font: "Georgia", color: BRAND.colors.chocolate },
    paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 0 } },
  { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
    run: { size: 28, bold: true, font: "Georgia", color: BRAND.colors.cocoa },
    paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 1 } },
  { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
    run: { size: 24, bold: true, font: "Arial", color: BRAND.colors.darkChocolate },
    paragraph: { spacing: { before: 160, after: 80 }, outlineLevel: 2 } }
]

// Default body style
default: { document: { run: { font: "Arial", size: 22, color: BRAND.colors.darkChocolate } } }

// Table header
shading: { fill: BRAND.colors.chocolate, type: ShadingType.CLEAR }
// with white text: color: "FFFFFF"

// Table body rows: alternate White and Cream
shading: { fill: BRAND.colors.cream, type: ShadingType.CLEAR }
```

**Page setup:** Letter size (12240 × 15840 DXA), 1" margins (1440 DXA), 1.15 line spacing.

---

## Presentation Creation (pptx)

Use with the `pptx` skill and html2pptx workflow. Apply these CSS variables:

```css
/* CraftedWell brand variables for html2pptx */
:root {
  /* Primary palette */
  --dark-chocolate: #3D2314;
  --chocolate: #5A2C10;
  --cocoa: #8B4A24;
  --caramel: #C07F43;
  --soft-gold: #D4A45A;
  --cream: #FDF8F3;
  --border: #E5D5C5;
  
  /* Semantic */
  --forest: #5A7A4A;
  --terracotta: #B85C38;
  --slate: #6B6B6B;
  
  /* Typography */
  --font-display: Georgia, serif;
  --font-body: Arial, sans-serif;
  
  /* Text colors */
  --text-primary: var(--dark-chocolate);
  --text-heading: var(--chocolate);
  --text-secondary: var(--cocoa);
  
  /* Backgrounds */
  --bg-primary: #FFFFFF;
  --bg-secondary: var(--cream);
  --bg-dark: var(--dark-chocolate);
}

/* Base styles */
body { font-family: var(--font-body); color: var(--text-primary); background: var(--bg-primary); }
h1, h2, h3 { font-family: var(--font-display); color: var(--text-heading); font-weight: bold; }

/* Slide titles: 32-44pt Georgia Bold in Chocolate */
.slide-title { font-size: 36px; font-family: var(--font-display); color: var(--chocolate); font-weight: bold; }

/* Section divider: Dark Chocolate background, white text */
.section-divider { background: var(--bg-dark); color: white; }

/* Accent bar: 8px Chocolate bar on left of content slides */
.accent-bar { width: 8px; background: var(--chocolate); }

/* Cards: Cream background, 6-8px rounded corners */
.card { background: var(--cream); border-radius: 6px; }

/* Quote slides: Cream background, Caramel quote mark */
.quote-mark { color: var(--caramel); font-size: 72px; font-family: var(--font-display); }
.quote-text { font-family: var(--font-display); font-style: italic; color: var(--text-primary); }
```

### Slide Layout Guidance

| Slide Type | Background | Key Styling |
|------------|------------|-------------|
| Title | White | Centered title (Georgia Bold 44pt), horizontal logo at bottom |
| Section | Dark Chocolate (#3D2314) | White text, centered |
| Content | White | 8px Chocolate accent bar left, title top-left |
| Quote | Cream | Large Caramel quote mark, italic Georgia text |
| Closing | Dark Chocolate | "Thank You" white, reversed logo |

### Charts

Use brand colors in order: Chocolate, Cocoa, Caramel, Soft Gold, Dark Chocolate.
For positive/negative: Forest (#5A7A4A) / Terracotta (#B85C38).

---

## Tables (All Formats)

| Part | Style |
|------|-------|
| Header | Chocolate (#5A2C10) background, white bold Arial text |
| Body | Alternating White / Cream (#FDF8F3) rows |
| Borders | 1pt #E5D5C5, horizontal only |
| Alignment | Text left, numbers right |
