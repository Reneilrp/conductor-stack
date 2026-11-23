---
name: hub
description: Central intelligence hub and meta-router for all coding and engineering tasks. Analyzes scope, intent, and complexity to automatically route to the right skill (Direct Fast-Path, federated-orchestrator, poteto-mode, architect, interrogate, how, why, arena). Use with /hub, /conductor, or as the default entry point.
---

# The Engineering Hub (Meta-Router)

The **Hub** is your single front door. Instead of manually remembering 58+ skills and slash commands, send any engineering goal to `/hub`.

The Hub evaluates your request against a strict **5-Tier Complexity Matrix**, prevents over-engineering, prints a **1-line Dispatch Receipt**, and routes directly to the optimal workflow.

---

## The 5-Tier Dispatch Matrix

When receiving a prompt, classify it into one of these 5 levels:

```
                          [User Prompt to /hub]
                                    │
                                    ▼
       ┌────────────────────────────┼───────────────────────────┐
       ▼                            ▼                           ▼
[Level 0: Direct Fast-Path]  [Level 1: Forensics]    [Level 2: Focused Task]
  • Typos, 1-line edits        • /how: mental models   • /poteto-mode
  • Plain syntax questions     • /why: git history     • 5-phase pstack state
  • Zero subagent overhead                             • Repro test + TDD fix
       │                            │                           │
       └────────────────────────────┼───────────────────────────┘
                                    │
       ┌────────────────────────────┴───────────────────────────┐
       ▼                                                        ▼
[Level 3: Multi-Feature Epic]                        [Level 4: High-Risk Review]
  • federated-orchestrator                             • /interrogate
  • 2+ interconnected features                         • Adversarial diff breaking
  • Gap-analysis -> Plan -> Worktrees                  • Auth, billing, concurrency
```

---

## Routing Guidelines

### Level 0: Direct Fast-Path (Zero Overhead)
* **Triggers:** Typo fixes, 1-file styling/copy edits, simple documentation updates, casual questions ("how does `Array.reduce` work?").
* **Action:** Do **NOT** invoke subagents, worktrees, or heavy playbooks. Answer or edit directly in the current turn.
* **Dispatch Receipt:**  
  `[Hub: Direct Fast-Path] Simple/isolated request detected. Executing immediately with zero subagent overhead.`

### Level 1: Read-Only Codebase Forensics & Profiling
* **Triggers:** "How does the auth token refresh work?", "Why do we have a timeout here?", "Where should this logic live?", "Audit project tech stack / declare architecture".
* **Action:**
  * For subsystem walkthroughs $\rightarrow$ Route to **`/how`**.
  * For historical archaeology $\rightarrow$ Route to **`/why`**.
  * For stack detection & `ARCHITECTURE.md` generation $\rightarrow$ Route to **`project-profiler`**.
* **Dispatch Receipt:**  
  `[Hub: Forensics (/how | /why | project-profiler)] Codebase intelligence task detected. Analyzing architecture and patterns.`

### Level 2: Focused Task, Bug Fix, or Refactor
* **Triggers:** A bug report, a performance regression, an internal refactoring, or a single isolated feature.
* **Action:** Route to **`poteto-mode`** and match the corresponding playbook (`bug-fix`, `feature`, `refactoring`, `perf-issue`). Enforce the 5-phase flow:
  1. *Audit:* Read-only root-cause analysis.
  2. *Repro:* Minimal failing reproduction test.
  3. *TDD:* Surgical minimal diff.
  4. *Proof:* Real runtime execution evidence (`principle-prove-it-works`).
  5. *Clean:* Strip debug comments (`/unslop`, `/no-comments`).
* **Dispatch Receipt:**  
  `[Hub: pstack Playbook (<Playbook Name>)] Focused engineering task detected. Activating 5-phase root-cause and TDD state machine.`

### Level 3: Architecture & Design Forks
* **Triggers:** "Design the API before writing code", "Which approach is better: A or B?", "Set up design tokens / 60-30-10 theme", "Mock this API", "Start local dev server / stack", "Audit document formatting / generate styled docx or pptx".
* **Action:**
  * For interface contracts $\rightarrow$ Route to **`/architect`**.
  * For competing implementations $\rightarrow$ Route to **`/arena`**.
  * For visual theme, typography, & 60-30-10 tokens $\rightarrow$ Route to **`design-tokens-generator`**.
  * For offline API stubs and fixtures $\rightarrow$ Route to **`api-mock-factory`**.
  * For local dev server automation & port checks $\rightarrow$ Route to **`dev-stack-orchestrator`**.
  * For document style auditing & DOCX/PPTX generation $\rightarrow$ Route to **`doc-craft-engine`**.
* **Dispatch Receipt:**  
  `[Hub: Foundation / Tooling (/architect | /arena | dev-stack | design-tokens | doc-craft)] Specialized foundation task detected. Executing with dedicated tooling.`

### Level 4: System Epics (2+ Interconnected Features)
* **Triggers:** Requests involving multiple interdependent features (e.g., *Dashboard + Logistics + Inventory + Messaging*).
* **Action:** Route to **`federated-orchestrator`** (`/federated-flow`):
  1. Dynamic gap-analysis (only ask about unresolved technical forks).
  2. Master Implementation Plan (`PLAN.md`) with shared Contract Spine.
  3. User approval checkpoint.
  4. Parallel feature execution in isolated Git worktrees.
  5. Integration Arbiter cross-feature E2E journey test.
* **Dispatch Receipt:**  
  `[Hub: Federated Multi-Feature] Detected 2+ interdependent features. Initiating gap-analysis and Master Implementation Plan...`

### Level 5: High-Risk Adversarial Review
* **Triggers:** "Review this PR", "Check this diff for bugs", security/auth changes, payment processing logic, concurrency.
* **Action:** Route to **`/interrogate`** to aggressively find race conditions, memory leaks, and unhandled edge cases.
* **Dispatch Receipt:**  
  `[Hub: Adversarial Review (/interrogate)] Critical code changes detected. Spawning skeptical reviewer to challenge diff boundaries.`

---

## Execution Protocol for the Agent

Whenever the user invokes `/hub <prompt>`:
1. **Emit the Dispatch Receipt** as your first sentence.
2. **Adopt the Routed Protocol immediately** in the same response without making the user re-prompt.
3. If the routed workflow requires an alignment gate (like `PLAN.md` in `federated-orchestrator`), present it cleanly and wait for user confirmation.
