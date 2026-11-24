# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-11-24

### Added
- **`journey-craft`**: Autonomous headless Playwright E2E journey synthesizer with built-in visual contrast and WCAG AA/AAA verification.
- **`incident-triage`**: Real-time crash and log forensic analyzer. Pinpoints culprit line numbers across Node/TS, Python, Rust, PHP, and Go with git blame context.
- **`flight-recorder`**: Autonomous release engineer calculating SemVer impact (1-5 risk score), generating publication-grade PR markdown, and maintaining `CHANGELOG.md`.
- **`env-sentinel`**: Zero-drift environment and secret synchronizer. Detects missing keys between code and `.env.example`, checks for secret leaks, and auto-syncs templates.
- **`til-vault`**: Persistent agent memory and ADR manager in `.agents/memory/vault.json` and canonical `DECISIONS.md` to prevent repeated agent mistakes.
- **`app-shield`**: Post-prototype security hardening and resilience engine. Audits XSS, CSRF, security headers, open CORS, and scaffolds custom 404/500 error boundaries.
- **Dev Stack Runners**: Added `scripts/dev.ps1` (PowerShell) and `scripts/dev.sh` (Bash) with port checks and graceful trap handlers.

### Changed
- **`hub`**: Expanded 5-Tier Dispatch Matrix with automated routes for forensics, intelligence, tooling, hardening, and release flight recording.
- **`AGENTS.md`**: Updated 5-Phase pstack protocol and Wave 3 integration with newly added tooling.
- **`README.md`**: Documented all new executive skills and capabilities.
