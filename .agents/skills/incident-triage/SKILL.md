---
name: incident-triage
description: Forensic analyzer and watcher for runtime crashes, stack traces, and build failures. Pinpoints culprit lines via git blame, isolates root causes, and scaffolds minimal reproduction tests. Use with /incident-triage, /triage, or during debugging.
---

# 🚨 Incident Triage — Real-Time Crash & Log Forensic Triager

**Incident Triage** transforms chaotic terminal crashes and stack traces into structured, actionable root-cause intelligence. It isolates the exact offending line, fetches source code context and `git blame` history, scaffolds a minimal reproduction test, and outputs the exact command to dispatch directly to `/hub`.

---

## ⚡ How It Works

```
[Raw Terminal Stack Trace / Log]
               │
               ▼
   [incident-triage Engine]
   ├─ Detects Runtime (Node/TS, Python, PHP, Rust, Go)
   ├─ Isolates Culprit File, Line & Column
   ├─ Inspects Surrounding Source Code
   ├─ Extracts Git Blame (Author, Commit, Summary)
   └─ Scaffolds Minimal Repro Test Stub
               │
               ▼
  [Ready-to-Run /hub Command]
```

---

## 🛠️ CLI Quickstart

### 1. Triage Directly from Piped Terminal Output
* **Windows (PowerShell):**
  ```powershell
  Get-Content error.log | py -3 .agents/skills/incident-triage/scripts/triage_log.py -
  ```
* **Linux / macOS:**
  ```bash
  cat error.log | python3 ~/.agents/skills/incident-triage/scripts/triage_log.py -
  ```

### 2. Triage a Log File & Scaffold a Minimal Repro Test
```powershell
py -3 .agents/skills/incident-triage/scripts/triage_log.py app_crash.log --out-repro tests/repro.test.ts
```

### 3. Triage Inline Text String
```powershell
py -3 .agents/skills/incident-triage/scripts/triage_log.py --text "TypeError: Cannot read properties of undefined (reading 'token') at AuthService.verify (src/auth/jwt.ts:42:15)"
```

---

## 🎯 Direct Bridge to `/hub`

The triage report automatically generates a Level 2 (`poteto-mode` 5-Phase) command formatted for `/hub`:
```text
/hub TypeError: Cannot read properties of undefined (reading 'token') in src/auth/jwt.ts:42. repro first, then fix and verify.
```
This guarantees you never skip Phase 1 (Root-Cause Audit & Repro Test) before applying code fixes!
