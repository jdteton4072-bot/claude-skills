---
name: steal
description: Clones UI designs, features, or code patterns from websites, screenshots, or app descriptions and implements them in your project. Use this skill when you see something you like on the web or in another product and want to replicate it.
---

# Steal

This skill analyzes UI designs, features, or code patterns from a reference source (URL, screenshot, or description) and implements a high-fidelity equivalent in your project — fully original code, no copying verbatim.

## When to Use This Skill

- Seeing a UI component on a website and wanting to replicate it
- Wanting a feature that works like one in another app
- Needing a design pattern (animation, layout, color scheme) for your project
- Replicating an interaction or micro-interaction from a live site
- Adapting landing page sections, dashboards, or widgets from references

## How to Use

### From a URL

```
/steal https://stripe.com/pricing — replicate their pricing table
```

```
/steal https://linear.app — steal their command palette
```

### From a Screenshot

```
/steal [paste screenshot] — build this layout for my React app
```

### From a Description

```
/steal the toast notification system from Vercel's dashboard
```

```
/steal the accordion FAQ section from this design
```

## Workflow

### Step 1: Capture the Reference

Accept one or more of:
- **URL** — use `WebFetch` to capture the page's HTML, CSS, and JS
- **Image/screenshot** — analyze layout, components, colors, typography, spacing, and interactions visually
- **Description** — ask clarifying questions to understand what specific element to replicate

### Step 2: Deconstruct

Analyze the reference and extract:

1. **Visual anatomy**
   - Layout structure (grid, flex, absolute positioning)
   - Component hierarchy
   - Color palette and typography scale
   - Spacing and sizing system

2. **Interaction model**
   - Hover, active, focus states
   - Animations and transitions (duration, easing, keyframes)
   - Keyboard navigation

3. **Data requirements**
   - What props/state the component needs
   - API shape if dynamic

Summarize findings in a brief **"What I'm stealing"** section before writing any code so the user can confirm scope.

### Step 3: Adapt and Implement

Implement a clean, original version using the user's existing stack. Defaults (ask if not clear from the repo):

| Concern | Default |
|---|---|
| Framework | React (TSX) |
| Styling | Tailwind CSS |
| Icons | Lucide |
| Animation | CSS transitions / Framer Motion |

Rules for implementation:

- Write original code — do NOT copy verbatim HTML/CSS/JS from the reference source
- Match the visual result and interaction feel, not the implementation internals
- Fit the user's existing conventions (component naming, file structure, import style)
- Keep components self-contained with clear props interfaces
- Use semantic HTML and accessible markup (ARIA roles, keyboard nav) by default

### Step 4: Show the Result

After implementing:

1. List the files created or modified
2. Show a usage example (JSX snippet or CLI invocation)
3. Note any dependencies the user needs to install
4. Flag any parts that couldn't be fully replicated and explain why

## Examples

### Example: Stripe-style Pricing Table

**User**: `/steal https://stripe.com/pricing — just the plan comparison cards`

**Output**:
```
What I'm stealing:
- 3-column card grid with a highlighted "recommended" center card
- Plan name, price, description, feature checklist, CTA button
- Hover lift effect on cards; border glow on recommended card
- Responsive: stack to 1 column on mobile

Implementing in React + Tailwind...
```

Creates `components/PricingTable.tsx` with full TypeScript props and responsive layout.

### Example: Linear Command Palette

**User**: `/steal the command palette from linear.app`

**Output**:
```
What I'm stealing:
- Keyboard shortcut (⌘K) to open a full-screen modal overlay
- Fuzzy search input at the top
- Grouped results list with keyboard navigation (↑↓ Enter Esc)
- Recent commands shown when input is empty

Implementing in React + Tailwind + cmdk...
```

Creates `components/CommandPalette.tsx` and a `useCommandPalette` hook.

### Example: Screenshot Input

**User**: `/steal [screenshot of a sidebar nav]`

**Output**:
```
What I'm stealing:
- Collapsible left sidebar with icon + label nav items
- Active item highlighted with accent color pill
- Section headers with muted labels
- Bottom section with user avatar and settings

Implementing...
```

## Tips

- Provide the most specific URL or screenshot you can — full-page URLs work but zoomed screenshots of the exact component are faster
- If the reference uses proprietary fonts or paid icons, an open-source substitute will be used and noted
- For complex animations, ask whether Framer Motion or pure CSS is preferred
- To steal from a native mobile app, provide a screen recording or screenshot

## What "Steal" Means Here

This skill produces **inspired, original implementations** — not plagiarism. It extracts design patterns and UX ideas (which aren't copyrightable) and writes fresh code. The goal is to save you the research and implementation time of figuring out how you'd build something similar.
