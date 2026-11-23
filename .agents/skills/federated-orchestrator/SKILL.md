---
name: federated-orchestrator
description: Multi-feature federated agent workflow for designing, planning, and executing interconnected features (e.g. dashboard, logistics, inventory, messaging) in parallel. Uses adaptive gap-analysis, contract-first architecture, visual design spines, isolated worktrees, and staged verification waves. Trigger with /federated-flow, /multi-feature, or whenever building 2+ interrelated features.
---

# Federated Multi-Feature Orchestration Protocol

Use this skill when building or expanding **multiple interrelated features** in an existing or greenfield project (e.g., adding *Dashboard, Logistics, Inventory, Messaging*).

It enforces a **Contract-First, Plan-Gated, Design-Consistent Federated Pipeline**.

---

## The 4-Stage Lifecycle

```
[User Request]
       │
       ▼
[Phase 1: Dynamic Gap-Analysis & Context Triage]
  ├── Detects existing backend & UI stack in repo
  ├── Locks user-specified choices (tech stack, design preferences)
  └── Evaluates Gaps:
        ├── Zero Gaps ───────────────► Skip to Phase 2
        └── Unresolved Forks/Design ──► Surgical Delta Interview
       │
       ▼
[Phase 2: Master Implementation Plan (PLAN.md)]
  ├── Section 1: Dual Contract Spine
  │     ├── 1A: Domain & Event Spine (types/, events/, API contracts)
  │     └── 1B: Visual Design Spine (Typography, 60-30-10 Color Scheme, Tokens)
  ├── Section 2: Strict Bounded Contexts (zero file overlap)
  ├── Section 3: Staged Execution Waves (Spines -> Worktrees -> Integration)
  └── Section 4: Measurable Done Criteria (E2E journey + visual audits)
       │
       ▼
[User Alignment Gate: Approval / Tweaks]
       │
       ▼
[Phase 3: Federated Wave Execution]
  ├── Wave 1: Chief Orchestrator (Writes Contract Spine, Design Tokens & Mock Adapters)
  ├── Wave 2: Parallel Feature Sub-Orchestrators (Isolated Git Worktrees)
  │            • Runs 5-phase pstack flow on Gemini 3.8 Flash (High Thinking)
  │            • Codes strictly against contract mocks and shared design tokens
  └── Wave 3: Integration Arbiter
               • Merges worktrees into staging branch
               • Replaces contract mocks with live implementations
               • Executes cross-feature End-to-End verification test & UI audit
       │
       ▼
[Phase 4: Sanitization & Clean Handoff] (/unslop, /no-comments, impeccable audit)
```

---

## Detailed Step-by-Step Execution

### Phase 1: Dynamic Gap-Analysis & Context Triage

Before proposing plans or asking questions, inspect the active environment:
1. **Check for `ARCHITECTURE.md`:** If `ARCHITECTURE.md` exists (generated via `project-profiler`), treat it as the immutable single source of truth for frontend, backend, database, and background services. Lock all declared technologies immediately.
2. **Analyze User Prompt:** Lock any explicitly stated stack, protocol, design theme, or color palette.
3. **Inspect Existing Codebase:** Read `package.json`, `composer.json`, ORM schemas, tailwind/CSS configs, existing theme files, and components.
4. **Identify Architectural & Visual Deltas:**
   * **Backend/Protocols:** Real-time mechanism (SSE vs. WS), external APIs (email, shipping), missing secrets.
   * **Visual Design System (If UI is involved):**
     * Does the project already have a `tailwind.config`, `tokens.ts`, or `DESIGN.md`?
     * If missing, identify the required **Typography Scale** and **3-Color Scheme (60-30-10 Rule)**:
       - **60% Dominant Base:** Neutral background / canvas / surface.
       - **30% Structural Secondary:** Harmonious card surfaces, borders, text, and sidebars.
       - **10% High-Contrast Accent:** Distinct, pop color deliberately contrasting with the base for critical visibility, active states, and CTAs.

#### Conditional Gate:
* **If Zero Gaps:** Immediately bypass interview and proceed to Phase 2.
* **If Gaps Exist:** Surface a **Surgical Delta Interview** with clear `(Recommended)` defaults and offline mock fallbacks.

---

### Phase 2: Master Implementation Plan (`PLAN.md`)

Draft a structured plan artifact containing:

1. **The Dual Contract Spine:**
   * **1A: Domain & Event Spine:** Shared interfaces (`types/`), event schemas (`StockLowEvent`), and API contracts.
   * **1B: Visual Design Spine (Design System):**
     * *Typography:* Font families (e.g. Inter + JetBrains Mono), scale (`text-xs` through `text-3xl`), and line heights.
     * *The 60-30-10 Palette:* Base neutral (60%), structural secondary (30%), and high-contrast accent (10%).
     * *Component Tokens:* Button variants, card containers, badge statuses (Success, Warning, Danger), input fields.
2. **Explicit Bounded Contexts:**
   * `src/features/inventory/` (owned by Inventory Agent).
   * `src/features/logistics/` (owned by Logistics Agent).
   * `src/features/messaging/` (owned by Messaging Agent).
   * `src/features/dashboard/` (owned by Dashboard Agent).
   * `src/shared/design/` (frozen design tokens, icons, and theme variables).
3. **Execution Waves & Mock Strategy:**
   * Define offline mock adapters for external APIs (Resend, Shippo, Stripe).
4. **Measurable Verification Criteria:**
   * Unit tests per feature + Cross-feature E2E journey test + Visual accessibility/contrast check.

---

### Phase 3: User Alignment Gate

Present the plan with the visual design palette preview and architectural boundaries. Wait for user approval before modifying code.

---

### Phase 4: Federated Wave Execution

#### Wave 1: The Dual Spine & Mock Adapters
* The Chief Orchestrator delegates to specialized leaf skills:
  1. Shared data contracts and event types (`src/shared/types/`).
  2. **`design-tokens-generator`:** Generates `src/shared/design/tokens.ts` (60-30-10 palette, typography scale, component tokens) and `DESIGN.md`.
  3. **`api-mock-factory`:** Generates offline in-memory mock adapters and seed fixtures (`src/shared/mocks/`).
* Zero feature business logic or individual feature UI is written here.

#### Wave 2: Parallel Feature Sub-Orchestrators (Isolated Worktrees)
* Dispatch parallel subagents in isolated Git worktrees.
* Each subagent builds its assigned feature strictly using:
  * The mock interfaces from **Spine 1A**.
  * The shared design tokens from **Spine 1B** (ensuring Dashboard, Logistics, Messaging, and Inventory share identical button shapes, fonts, and colors).
* Subagents enforce the 5-phase `pstack` flow on **Gemini 3.8 Flash (High Thinking)**.

#### Wave 3: Integration Arbiter & E2E Proof
* Merge feature worktrees into the integration branch.
* Swap contract mock adapters with live implementations.
* Execute the End-to-End System Journey Test.
* Audit visual consistency and WCAG contrast across all four screens (via `impeccable` or visual audit).
* Apply `/unslop` and `/no-comments`.
