---
name: project-profiler
description: Audits an existing project's repository, detects frontend, backend, database, ORM, services, and directory patterns, and generates/updates a canonical ARCHITECTURE.md manifesto. Use with /profile-project, /declare-stack, or when opening an unfamiliar repo.
---

# Project Architecture Profiler & Declarant

Use this skill whenever you open a new or existing repository, or before running complex multi-feature workflows (`federated-orchestrator`, `poteto-mode`).

Instead of forcing you to re-explain your stack or having agents scan files on every single prompt, this skill audits the repository and generates an authoritative **`ARCHITECTURE.md`** manifesto in the project root.

---

## What It Detects and Declares

```
┌────────────────────────────────────────────────────────┐
│                   ARCHITECTURE.md                      │
├───────────────────┬────────────────────────────────────┤
│ 1. Frontend       │ Framework, Styling, State, Routing │
│ 2. Backend        │ Language, Framework, API Protocol  │
│ 3. Data & ORM     │ Database Engine, ORM, Cache/Queues │
│ 4. Topology       │ Monorepo vs Monolith, Folders      │
│ 5. Dev Services   │ Reverb WS, Celery, Ports, Runners  │
└───────────────────┴────────────────────────────────────┘
```

---

## How It Works

### Step 1: Run the Stack Scanner
Run the bundled audit script:
* **On Windows:**
  ```powershell
  py -3 .agents/skills/project-profiler/scripts/detect_stack.py . ARCHITECTURE.md
  ```
* **On Linux / WSL:**
  ```bash
  python3 ~/.agents/skills/project-profiler/scripts/detect_stack.py . ARCHITECTURE.md
  ```

### Step 2: Review & Refine
The scanner checks:
* `package.json`, `pnpm-lock.yaml`, `bun.lockb` $\rightarrow$ Next.js, Vite, React, Vue, Tailwind, Zustand, Prisma.
* `composer.json`, `artisan` $\rightarrow$ Laravel, Eloquent, Laravel Reverb, Pest/PHPUnit.
* `requirements.txt`, `pyproject.toml` $\rightarrow$ FastAPI, Django, Celery, SQLAlchemy.
* `schema.prisma`, `drizzle.config.*` $\rightarrow$ Database engine (Postgres, MySQL, SQLite).
* Folder layout $\rightarrow$ `src/features/` vs `controllers/` vs `app/`.

If anything is custom or un-detectable, it asks a single brief multiple-choice confirmation before writing.

### Step 3: Canonical Manifesto Output (`ARCHITECTURE.md`)
Writes the structured specification to the repository root.

---

## How Other Skills Consume `ARCHITECTURE.md`

1. **`federated-orchestrator` (`/federated-flow`):**
   * Reads `ARCHITECTURE.md` first.
   * **Bypasses the entire Gap-Analysis interview phase** because the stack, ORM, and protocols are already locked!
2. **`dev-stack-orchestrator` (`/dev-stack`):**
   * Reads the background services (e.g. Reverb, Queue worker) and generates the startup scripts instantly.
3. **`poteto-mode` & `/architect`:**
   * Enforces type definitions and boundary contracts matching the declared stack without inventing conflicting libraries.

---

## Summary of Commands

| Command | Purpose |
|---|---|
| `/profile-project` | Audits the current repository and writes `ARCHITECTURE.md`. |
| `/declare-stack` | Interactive wizard to declare or update the project's stack. |
