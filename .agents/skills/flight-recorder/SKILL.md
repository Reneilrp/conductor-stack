---
name: flight-recorder
description: Autonomous release engineer that inspects git diffs against base branches, determines SemVer impact, updates CHANGELOG.md, and generates publication-grade Pull Request descriptions with risk assessments. Use with /flight-recorder, /ship-it, or before merging.
---

# 🛫 Flight Recorder — Autonomous Release, PR & Changelog Engine

**Flight Recorder** automates the final delivery milestone of feature branches. It eliminates manual PR drafting, SemVer guessing, and forgotten changelogs. By diffing your current working branch against your base branch (`main`/`master`), it calculates blast-radius risk, classifies breaking changes, updates `CHANGELOG.md`, and compiles a publication-ready `PULL_REQUEST.md`.

---

## ⚡ What It Automates

1. **SemVer Impact Analysis:** Inspects commit messages and changed files to determine whether the release is `MAJOR` (breaking), `MINOR` (features), or `PATCH` (fixes/refactors).
2. **Blast Radius Scoring (1–5):** Analyzes file volume and detects touches to sensitive subsystems (schemas, migrations, auth, encryption).
3. **Publication-Grade PR Markdown (`PULL_REQUEST.md`):** Formats an executive summary, file impact table, risk score, and testing proof checklist.
4. **Changelog Prepending:** Updates `CHANGELOG.md` following [Keep a Changelog](https://keepachangelog.com/) standards.

---

## 🛠️ CLI Quickstart

### 1. Compile PR & Update Changelog
* **Windows (PowerShell):**
  ```powershell
  py -3 .agents/skills/flight-recorder/scripts/record_flight.py
  ```
* **Linux / macOS:**
  ```bash
  python3 ~/.agents/skills/flight-recorder/scripts/record_flight.py
  ```

### 2. Compare Against a Specific Base Branch
```powershell
py -3 .agents/skills/flight-recorder/scripts/record_flight.py --base develop --pr-out PR.md
```

### 3. Print Directly to Terminal Without Writing
```powershell
py -3 .agents/skills/flight-recorder/scripts/record_flight.py --stdout --skip-changelog
```

---

## 🎯 Integration in Federated Flows

In **Wave 3 (Integration Arbiter & Release)** of `federated-orchestrator`, run `record_flight.py` right before merging feature worktrees to guarantee full traceability and clean documentation.
