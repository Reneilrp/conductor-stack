# Coding Agent Architecture: pstack Flow Protocol

This workspace enforces a **Homogeneous Model, Heterogeneous Personas** sub-orchestration pipeline powered by **pstack** principles and **Gemini 3.8 Flash (High Thinking Effort)**.

---

## 1. Core Operating Model
* **Model Engine:** All orchestration, subagents, audits, and implementations run on **Gemini 3.8 Flash with High Thinking Effort**.
* **Cognitive Strategy:** Quality and rigor are achieved through **phased subagent isolation** and **strict verification gates**, eliminating confirmation bias and "AI slop".
* **Routing Standard:**
  * **Primary Universal Entry Point:** `/hub` (The Central Intelligence Hub & Meta-Router). Automatically inspects scope and dispatches the optimal route.
  * For single tasks, bug fixes, single features, or refactors $\rightarrow$ Follow the **5-Phase Sub-Orchestration Flow** (Section 2 via `/poteto-mode`).
  * For 2+ interconnected features (e.g. Dashboard, Logistics, Inventory, Messaging) $\rightarrow$ Follow the **Federated Multi-Feature Flow** (Section 3 via `/federated-flow`).

---

## 2. The 5-Phase Sub-Orchestration Flow (Single Tasks / Bug Fixes)

Whenever tackling any focused bug, feature, refactor, or performance issue, follow this sequential state machine:

### Phase 1: Audit & Root-Cause (Read-Only)
* **Tools / Skills:** `/how`, `/why`, `principle-fix-root-causes`
* **Protocol:**
  1. Inspect codebase architecture and trace history without altering production code.
  2. Locate the precise root cause.
  3. Write a standalone minimal reproduction test or script that fails.
* **Gate Check:** You are strictly forbidden from modifying production files until the reproduction test reproduces the failure.

### Phase 2: Architectural Contract & Boundary Design
* **Tools / Skills:** `/architect`, `principle-foundational-thinking`, `principle-model-the-domain`
* **Protocol:**
  1. Map types, contracts, and function boundaries before writing logic.
  2. Make illegal states unrepresentable.
  3. Apply `principle-subtract-before-you-add`: identify dead weight or obsolete helpers to prune first.
* **Gate Check:** The data shape and boundary contract must be settled before implementation starts.

### Phase 3: Surgical Implementation (TDD)
* **Tools / Skills:** `/tdd`, `principle-laziness-protocol`, `principle-boundary-discipline`
* **Protocol:**
  1. Write the minimal code required to turn the Phase 1 reproduction test green.
  2. Bias toward the smallest possible diff.
  3. Trust internal types; place validations only at external boundaries.
* **Gate Check:** All unit and reproduction tests pass locally.

### Phase 4: Adversarial Verification
* **Tools / Skills:** `/interrogate`, `principle-prove-it-works`, `principle-test-behavior-not-implementation`
* **Protocol:**
  1. Review the diff with a skeptical, adversarial posture ("try to break this fix").
  2. Test edge cases, concurrency, and boundary conditions.
  3. Execute the real runtime command or test suite and inspect raw output.
* **Gate Check:** "It compiles" or "looks good" is never accepted. Real runtime execution evidence must be logged.

### Phase 5: Sanitization & Clean Handoff
* **Tools / Skills:** `/unslop`, `/no-comments`, `technical-writing`
* **Protocol:**
  1. Strip all temporary debugging comments, console logs, and workaround tags (`/no-comments`).
  2. Tighten prose to remove AI conversational filler (`/unslop`).
  3. Format concise, conventional commit messages and review summaries.

---

## 3. The Federated Multi-Feature Flow (2+ Interconnected Features)
* **Primary Skill:** `federated-orchestrator` (`/federated-flow`, `/multi-feature`)

When the user requests multiple interdependent features (e.g. *Dashboard + Logistics + Inventory + Messaging*), execute this 4-stage federated pipeline:

### Step 1: Dynamic Gap-Analysis & Context Triage
* **Lock User Choices:** Any stack, protocol, or provider explicitly named by the user is locked immediately. Never re-interview what the user already stated.
* **Inspect Codebase First:** Detect existing frameworks, ORMs, and `.env` credentials in the repo before asking questions.
* **Conditional Interview:**
  * If zero gaps exist $\rightarrow$ Bypass interview; proceed directly to Step 2.
  * If critical architectural gaps or missing API credentials exist $\rightarrow$ Ask a surgical, multiple-choice Delta Interview with clear `(Recommended)` defaults and offline mock fallbacks.

### Step 2: Master Implementation Plan (`PLAN.md`)
* Produce a structured implementation blueprint containing:
  1. **Dual Contract Spine:** 
     * **1A. Domain Spine:** Shared data models, events, and API interfaces (`types/`, `events/`).
     * **1B. Visual Design Spine:** Typography scale, 60-30-10 color scheme (60% neutral canvas, 30% structural secondary, 10% high-contrast accent for visibility), and shared UI tokens.
  2. **Bounded Contexts:** Explicit file partitions per feature (zero cross-file collisions).
  3. **Execution Waves:** Wave 1 (Dual Spines & Mocks) $\rightarrow$ Wave 2 (Parallel Worktrees using shared tokens) $\rightarrow$ Wave 3 (Integration & Visual Audit).
  4. **Measurable Verification:** End-to-end journey tests and contrast/consistency checks that must pass.
* **User Alignment Gate:** Halt and wait for user approval or adjustments before modifying code.

### Step 3: Federated Wave Execution
1. **Wave 1 (Dual Spine & Mocks):** Chief Orchestrator writes shared domain schemas and delegates to specialized leaf skills: `design-tokens-generator` (60-30-10 palette, typography scale, tokens) and `api-mock-factory` (in-memory mock adapters and seed fixtures).
2. **Wave 2 (Parallel Feature Worktrees):** Parallel subagents run in isolated Git worktrees against the mock contracts and shared design tokens, each enforcing the 5-Phase pstack flow.
3. **Wave 3 (Integration Arbiter & E2E Proof):** Merge branches, wire live dependencies together, and execute the full cross-feature journey test and visual audit.

### Step 4: Polish & Handoff
* Apply `/unslop` and `/no-comments` across the integrated diff.

---

## 4. Guiding Principles Reference
* **`prove-it-works`:** Always verify against the real artifact and inspect actual runtime results.
* **`fix-root-causes`:** Never patch symptoms with defensive nil-checks; fix the source.
* **`laziness-protocol`:** Bias toward code deletion and the smallest diff that solves the root problem.
* **`guard-the-context-window`:** Use fresh subagent contexts for separate phases to avoid confirmation bias.
* **`model-the-domain`:** Encode domain constraints in shared data models and types before writing features.
