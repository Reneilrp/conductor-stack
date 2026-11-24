---
name: app-shield
description: Post-prototype security hardening & UX resilience engine. Audits codebases for XSS, CSRF, open CORS, missing HTTP security headers, and scaffolds production-ready custom 404 pages, global error boundaries, and security middleware. Use with /app-shield, /harden, or during Phase 4 verification.
---

# 🛡️ App Shield — Post-Prototype Hardening & Security Resilience Engine

**App Shield** bridges the critical gap between rapid prototyping and production deployment. When developing fast prototypes, developers and autonomous agents frequently bypass security headers, omit CSRF defenses, leave raw XSS injection points, use wildcard CORS (`*`), and forget custom 404/500 error boundaries.

App Shield audits the application for these vulnerabilities and scaffolds production-ready protections tailored to the detected framework (Next.js, React/Vite, Laravel, FastAPI, Express).

---

## ⚡ What It Audits & Scaffolds

```
┌────────────────────────────────────────────────────────┐
│                   APP SHIELD SUITE                     │
├───────────────────────┬────────────────────────────────┤
│ 1. UX Resilience      │ Custom 404 page & Error        │
│                       │ boundaries without stack leaks │
├───────────────────────┼────────────────────────────────┤
│ 2. Security Headers   │ CSP, HSTS, X-Frame-Options,    │
│                       │ X-Content-Type-Options: nosniff│
├───────────────────────┼────────────────────────────────┤
│ 3. Injection Defense  │ XSS, dangerouslySetInnerHTML,  │
│                       │ raw v-html, innerHTML vectors  │
├───────────────────────┼────────────────────────────────┤
│ 4. Boundary Control   │ Strict CORS origin enforcement │
│                       │ and rate-limiting middleware   │
└───────────────────────┴────────────────────────────────┘
```

---

## 🛠️ CLI Quickstart

### 1. Run Static Security & Resilience Audit
Inspects the current repository and outputs a readiness scorecard with letter grade (A–F):
* **Windows (PowerShell):**
  ```powershell
  py -3 .agents/skills/app-shield/scripts/shield_engine.py --audit
  ```
* **Linux / macOS:**
  ```bash
  python3 ~/.agents/skills/app-shield/scripts/shield_engine.py --audit
  ```

### 2. Auto-Scaffold Missing Assets
Instantly creates missing production error pages and security middleware:
* **Scaffold custom 404 page:**
  ```powershell
  py -3 .agents/skills/app-shield/scripts/shield_engine.py --scaffold 404
  ```
* **Scaffold global error boundary (500):**
  ```powershell
  py -3 .agents/skills/app-shield/scripts/shield_engine.py --scaffold error
  ```
* **Scaffold HTTP security headers:**
  ```powershell
  py -3 .agents/skills/app-shield/scripts/shield_engine.py --scaffold headers
  ```
* **Scaffold all missing assets at once:**
  ```powershell
  py -3 .agents/skills/app-shield/scripts/shield_engine.py --scaffold all
  ```

### 3. CI / Pre-Release Strict Gate
Fails with exit code 1 if hardening score is below 80%:
```powershell
py -3 .agents/skills/app-shield/scripts/shield_engine.py --strict
```

---

## 🎯 Workflow Placement

* **`poteto-mode` (Phase 4: Adversarial Verification):** Run `shield_engine.py --audit` alongside `/interrogate` before claiming a feature or refactor is ready.
* **`federated-orchestrator` (Wave 2.5):** Run before Wave 3 integration to ensure all parallel branches adhere to security and error boundary standards.
* **`/hub`:** Triggers automatically whenever you ask to *"harden this prototype"*, *"check security"*, or *"add 404/error pages"*.
