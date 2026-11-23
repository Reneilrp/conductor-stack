---
name: design-tokens-generator
description: Generates production-ready design tokens, typography pairings, and accessible 60-30-10 color palettes (60% neutral base, 30% structural surface, 10% high-contrast accent) with WCAG AAA contrast guarantees. Use standalone or as Wave 1 leaf skill in federated-orchestrator.
---

# Design Tokens Generator

Use this skill whenever setting up a new design system, theme, or visual spine for multi-feature UI development. It produces a **single source of visual truth** (`tokens.ts` and `DESIGN.md`) so that parallel feature agents build visually coherent interfaces without CSS conflicts or mismatched aesthetics.

---

## The 60-30-10 Color Architecture

Every generated palette follows the strict **60-30-10 Rule** to guarantee visual calm paired with immediate operational visibility:

```
┌────────────────────────────────────────────────────────┐
│  60% Dominant Base (Canvas & Neutral)                  │
│  • Page backgrounds, canvas, subtle borders, muted text│
│                                                        │
│  ┌──────────────────────────────────────────────┐      │
│  │  30% Structural Secondary (Surfaces)         │      │
│  │  • Cards, modals, sidebars, input containers │      │
│  │  • Harmonious with the 60% base              │      │
│  │                                              │      │
│  │  ┌────────────────────┐                      │      │
│  │  │  10% High-Contrast │                      │      │
│  │  │  Accent (Action)   │                      │      │
│  │  │  • CTAs, badges    │                      │      │
│  │  │  • Active alerts   │                      │      │
│  │  └────────────────────┘                      │      │
│  └──────────────────────────────────────────────┘      │
└────────────────────────────────────────────────────────┘
```

1. **60% Dominant Base (Neutral Canvas):**
   * *Dark Mode:* Deep charcoal/zinc (`#09090b` or `#0f172a`).
   * *Light Mode:* Soft off-white/zinc (`#f8fafc` or `#f4f4f5`).
   * *Rule:* Never pure harsh black `#000` or blinding raw white `#fff` without slight warmth/coolness.

2. **30% Structural Secondary (Harmonious Surfaces):**
   * *Purpose:* Defines containers, table headers, sidebars, cards, and modal sheets.
   * *Rule:* Must blend harmoniously with the 60% base (typically 1–2 tonal steps lighter in dark mode, or 1–2 steps darker/elevated in light mode).

3. **10% High-Contrast Accent (Pop & Visibility):**
   * *Purpose:* The focal point. Reserved strictly for Primary Buttons, Active State Indicators, Status Badges, and Critical Alerts.
   * *Rule:* **Deliberately high-contrast.** It must pop out against both the 60% and 30% layers (e.g. Electric Amber, Bright Emerald, or Vivid Indigo). Must pass **WCAG AA (4.5:1)** for text and **3:1** for UI components.

---

## Typography Pairings & Strict Scale

Every generated token set establishes three font categories and a modular type scale:

| Category | Recommended Pairings | Usage |
|---|---|---|
| **Display / Heading** | Plus Jakarta Sans, Geist, Space Grotesk, Inter | Page titles, card headers, metric stat numbers |
| **Body / UI** | Inter, Geist Text, System Sans-Serif | Paragraphs, labels, button text, table cells |
| **Monospace / Data** | JetBrains Mono, Fira Code, Roboto Mono | SKU codes, tracking numbers, timestamps, monetary values |

### Strict Modular Scale:
* `text-xs`: 12px / 16px (Badges, metadata captions)
* `text-sm`: 14px / 20px (Standard UI labels, table rows, button text)
* `text-base`: 16px / 24px (Body text, card descriptions)
* `text-lg`: 18px / 28px (Section titles, subheadings)
* `text-xl`: 20px / 28px (Modal titles, card headers)
* `text-2xl`: 24px / 32px (Page headers, high-level metrics)

---

## Output Deliverables

When invoked, this skill writes two canonical files in the workspace:

### 1. `src/shared/design/tokens.ts` (or Tailwind theme extension)
```typescript
export const tokens = {
  colors: {
    base: {
      canvas: "var(--color-canvas)",
      muted: "var(--color-muted)",
    },
    surface: {
      card: "var(--color-card)",
      border: "var(--color-border)",
      sidebar: "var(--color-sidebar)",
    },
    accent: {
      primary: "var(--color-accent-primary)",
      primaryHover: "var(--color-accent-primary-hover)",
      contrastText: "var(--color-accent-text)",
    },
    status: {
      success: "#10b981",
      warning: "#f59e0b",
      danger: "#ef4444",
      info: "#3b82f6",
    }
  },
  typography: {
    fontDisplay: "var(--font-display)",
    fontBody: "var(--font-body)",
    fontMono: "var(--font-mono)",
  },
  spacing: {
    cardPadding: "1.25rem",
    inputHeight: "2.5rem",
  },
  radius: {
    sm: "0.25rem",
    md: "0.5rem",
    lg: "0.75rem",
  }
} as const;
```

### 2. `DESIGN.md`
A human-readable and agent-readable Markdown artifact summarizing color swatches, font pairings, component anatomy, and WCAG contrast audit results.
