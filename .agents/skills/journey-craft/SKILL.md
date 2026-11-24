---
name: journey-craft
description: Synthesizes headless Playwright E2E journey tests, form interactions, and WCAG AA/AAA visual contrast verification suites from declared routes and contracts. Use with /journey-craft, /e2e-craft, or as Wave 3 Integration Arbiter in federated-orchestrator.
---

# 🚀 Journey Craft — Autonomous E2E Journey & Accessibility Synthesizer

**Journey Craft** eliminates the manual toil of authoring end-to-end integration tests. It scans your application routes or consumes the `Dual Contract Spine` from `federated-orchestrator`, then generates production-ready Playwright test suites with built-in visual contrast and WCAG AA/AAA compliance checks.

---

## 🧠 Why Journey Craft?

In modern multi-agent development:
1. **Wave 1 & 2** build components, design tokens, and mock APIs in parallel.
2. **Wave 3 (Integration Arbiter)** requires verified proof that all features actually work together without breaking navigation or causing unreadable low-contrast UI.
3. Journey Craft serves as the automated test authoring engine for Wave 3.

---

## 🛠️ CLI Quickstart

Run the bundled synthesizer:

### 1. Auto-Scan & Generate Playwright TypeScript Tests
* **Windows (PowerShell):**
  ```powershell
  py -3 .agents/skills/journey-craft/scripts/craft_journey.py --base-url http://localhost:3000 --out-dir tests/e2e
  ```
* **Linux / macOS:**
  ```bash
  python3 ~/.agents/skills/journey-craft/scripts/craft_journey.py --base-url http://localhost:3000 --out-dir tests/e2e
  ```

### 2. Explicit Custom Routes
Provide specific routes directly:
```powershell
py -3 .agents/skills/journey-craft/scripts/craft_journey.py --routes / /dashboard /inventory /settings --lang ts
```

### 3. Generate Python Playwright Suite
```powershell
py -3 .agents/skills/journey-craft/scripts/craft_journey.py --lang py --out-dir tests/e2e
```

---

## 📋 Generated Capabilities

Every generated suite includes:
- **Route Sanity Matrix:** Ensures all detected pages return `< 400` status codes and no unhandled 404/500 screens.
- **Visual Contrast Verification:** Automatically inspects rendered text elements (`h1`, `p`, `button`, etc.) to guarantee text colors do not collide with background colors.
- **Automated Viewport Screenshots:** Saves failure and milestone screenshots into `test-results/screenshots/`.
- **Form & Navigation Resilience:** Tests navbar links and input field editability.
