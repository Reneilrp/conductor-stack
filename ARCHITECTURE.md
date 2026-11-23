# Project Architecture & Tech Stack: Automation

> **Notice for Coding Agents:** This file is the authoritative architectural blueprint for this codebase. Before proposing, adding, or modifying features, adhere to the technologies, patterns, and boundaries declared below.

---

## 1. Core Technology Stack

| Layer | Technology | Details |
|---|---|---|
| **Frontend** | None / Static | Styling: Standard/CSS · State: None |
| **Backend** | None / Serverless | Language: N/A |
| **Database & ORM** | TBD | ORM: None / Raw SQL |
| **Dev Tooling** | Package Mgr: N/A | Test Runner: None detected |

---

## 2. Architecture & Directory Boundaries
- **Project Type:** Standard Monolith
- **Discovered Key Folders:** Flat / Root structure

---

## 3. Background Services & Daemons
- No dedicated background worker daemons detected.

---

## 4. Architectural Rules for Autonomous Agents
1. **Never introduce conflicting runtimes:** Use the established ORM and frameworks listed above.
2. **Honor boundary partitions:** Place shared logic in `src/shared/` or common service directories.
3. **Respect directory layout:** Do not invent alternative module folders when canonical ones exist above.