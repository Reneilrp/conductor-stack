---
name: til-vault
description: Persistent memory vault and Architecture Decision Record (ADR) manager. Records tooling quirks, architectural decisions, and post-mortem lessons so agents never repeat past mistakes. Use with /til-vault, /til, /adr, or during post-fix handoff.
---

# 🧠 TIL Vault — Persistent Agent Memory & ADR Manager

**TIL Vault** solves the stateless limitation of AI coding agents. When an agent resolves a tricky platform quirk, establishes a crucial domain contract, or refactors a complex module, TIL Vault records the lesson into `.agents/memory/vault.json` and updates `DECISIONS.md`.

Whenever `/hub` plans a new task, it queries this vault to ensure historical constraints and past bugs are never reintroduced.

---

## ⚡ Memory Categories

1. **`adr` (Architecture Decision Record):** Records foundational design choices (e.g., choosing Zustand over Redux, choosing UUIDv7 over Auto-increment, or separating read/write models).
2. **`quirk` (Platform & Tooling Quirks):** Records OS or environment-specific workarounds (e.g., Windows PowerShell quote escaping, Docker volume permissions on WSL2, port-forwarding issues).
3. **`lesson` (Post-Mortem Fixes):** Captures the root cause and lessons learned from difficult bugs resolved during `poteto-mode` Phase 5.

---

## 🛠️ CLI Quickstart

### 1. Record an Architecture Decision Record (ADR)
* **Windows (PowerShell):**
  ```powershell
  py -3 .agents/skills/til-vault/scripts/vault_cli.py record --title "Adopt UUIDv7 for Database Primary Keys" --category adr --tags database uuid postgres --content "UUIDv7 provides time-ordered indexing while retaining global uniqueness, eliminating B-tree fragmentation."
  ```
* **Linux / macOS:**
  ```bash
  python3 ~/.agents/skills/til-vault/scripts/vault_cli.py record --title "Adopt UUIDv7" --category adr --content "..."
  ```

### 2. Record a Platform Quirk
```powershell
py -3 .agents/skills/til-vault/scripts/vault_cli.py record --title "PowerShell curl alias is Invoke-WebRequest" --category quirk --tags powershell windows curl --content "Always call curl.exe explicitly or use Invoke-RestMethod on Windows to avoid parameter collision."
```

### 3. Search Vault by Keyword
```powershell
py -3 .agents/skills/til-vault/scripts/vault_cli.py query "powershell"
```

### 4. Compile Canonical `DECISIONS.md`
Exports all records into a single authoritative markdown document in the repository root:
```powershell
py -3 .agents/skills/til-vault/scripts/vault_cli.py export-adr --out DECISIONS.md
```

### 5. Ingest Summary into `/hub`
```powershell
py -3 .agents/skills/til-vault/scripts/vault_cli.py summary
```
