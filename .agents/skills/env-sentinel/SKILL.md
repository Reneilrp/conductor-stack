---
name: env-sentinel
description: Audits codebases for environment variable drift, secret leaks, and missing configuration keys. Synchronizes .env and .env.example with zero-drift safety checks. Use with /env-sentinel, /audit-env, or as pre-flight check in dev-stack.
---

# 🛡️ Env Sentinel — Zero-Drift Secret & Environment Synchronizer

**Env Sentinel** guarantees that your local environment variables, `.env.example` templates, and source code are always in 100% synchronization. It prevents painful "works on my machine" failures, missing keys during agent execution, and dangerous leaks of live API tokens or credentials into git.

---

## ⚡ What It Audits

```
┌────────────────────────────────────────────────────────┐
│                   ENV SENTINEL AUDIT                   │
├───────────────────────┬────────────────────────────────┤
│ 1. Codebase Scan      │ Finds process.env, os.environ, │
│                       │ env(), getenv(), docker vars   │
│ 2. Drift Detection    │ Missing in .env.example vs code│
│ 3. Missing in Local   │ Declared in example but absent │
│ 4. Orphaned Keys      │ Declared in example, unused    │
│ 5. Secret Leak Guard  │ Catches live Stripe, AWS, Git  │
│                       │ and database connection strings│
└───────────────────────┴────────────────────────────────┘
```

---

## 🛠️ CLI Quickstart

### 1. Run Diagnostic Audit
* **Windows (PowerShell):**
  ```powershell
  py -3 .agents/skills/env-sentinel/scripts/audit_env.py
  ```
* **Linux / macOS:**
  ```bash
  python3 ~/.agents/skills/env-sentinel/scripts/audit_env.py
  ```

### 2. Auto-Synchronize `.env.example`
Automatically appends missing environment variables found in your code to `.env.example` with safe placeholder comments and type hints:
```powershell
py -3 .agents/skills/env-sentinel/scripts/audit_env.py --sync
```

### 3. CI / Strict Mode Pre-Flight Check
Fails with exit code 1 if any missing variables or leaked secrets are detected:
```powershell
py -3 .agents/skills/env-sentinel/scripts/audit_env.py --strict
```

---

## 🚀 Pre-Flight Integration in `dev-stack`

Before booting multi-service stacks or running `dev.ps1` / `dev.sh`, `env-sentinel` can run as a fast pre-flight verification to confirm all required environment variables are set before ports are bound.
