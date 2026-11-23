---
name: dev-stack-orchestrator
description: Inspects local project stacks, detects port conflicts, and generates clean cross-platform automation scripts to run backend, frontend, queue workers, and WebSocket servers (e.g. Laravel Reverb, Vite, Celery, Redis). Use with /dev-stack, /run-stack, or when starting local development environments.
---

# Dev Stack Orchestrator

Use this skill whenever you need to start, manage, or automate a multi-service local development environment. 

Instead of opening 4 separate terminal tabs to manually start your backend, frontend, worker, and WebSocket server, this skill audits your repository, inspects ports, and generates **unified, dual-platform startup scripts** (`scripts/dev.ps1` for Windows and `scripts/dev.sh` for WSL/Linux) with graceful shutdown handling.

---

## The 4-Phase Lifecycle

```
[Inspect Repository] ──► [Port & Process Audit] ──► [Generate Automation Scripts] ──► [Verify Health]
  • Backend runtime        • Check bound ports        • scripts/dev.ps1 (Windows)       • HTTP 200 ping
  • Frontend tooling       • Identify dead locks      • scripts/dev.sh (WSL/Linux)      • WS handshake
  • Workers & WebSockets   • Free orphaned PIDs       • Traps Ctrl+C for clean kill     • Status report
```

---

## Phase 1: Repository & Service Topology Detection

Before writing scripts, inspect the repo to map all required processes:

### Common Detection Signatures:
1. **Laravel Full-Stack:**
   * **Backend API:** `artisan` present $\rightarrow$ `php artisan serve --port=8000`
   * **WebSocket Server:** `config/reverb.php` or `composer.json` has `laravel/reverb` $\rightarrow$ `php artisan reverb:start`
   * **Queue Worker:** `app/Jobs/` or queue configured $\rightarrow$ `php artisan queue:work` or `queue:listen`
   * **Frontend Dev Server:** `vite.config.*` present $\rightarrow$ `npm run dev` or `pnpm dev`
2. **Node / Next.js / Monorepos:**
   * Root or nested `package.json` with `dev`, `start`, `watch`.
3. **Python / FastAPI / Django:**
   * `uvicorn app.main:app --reload` or `python manage.py runserver` + `celery -A app worker`.
4. **Infra Dependencies (Redis, Database):**
   * Check if Docker Compose (`docker-compose.yml`) or local service is expected.

---

## Phase 2: Port & Process Conflict Check

Check whether target ports are already occupied to avoid silent crash loops:

* **On Windows (PowerShell):**
  ```powershell
  Get-NetTCPConnection -LocalPort 8000, 5173, 8080 -ErrorAction SilentlyContinue | Select-Object LocalPort, OwningProcess, State
  ```
* **On Linux / WSL (Bash):**
  ```bash
  ss -tulpn | grep -E ':8000|:5173|:8080'
  ```

If an orphaned process is holding a port, report the PID and ask or offer to kill it cleanly.

---

## Phase 3: Generate Automation Scripts

Generate two robust, cross-platform scripts in the project's `scripts/` folder:

### 1. Windows Runner: `scripts/dev.ps1`
Must support background jobs, color-coded logging, and a clean shutdown trap:
```powershell
# scripts/dev.ps1
Write-Host "🚀 Starting Local Dev Stack..." -ForegroundColor Cyan

$processes = @()

function Start-DevService($name, $cmd, $args) {
    Write-Host "  Starting $name..." -ForegroundColor Yellow
    $p = Start-Process -FilePath $cmd -ArgumentList $args -NoNewWindow -PassThru
    return $p
}

try {
    # Example Laravel + Reverb + Vite Stack:
    $processes += Start-DevService "Backend" "php" "artisan serve --port=8000"
    $processes += Start-DevService "Reverb WS" "php" "artisan reverb:start"
    $processes += Start-DevService "Worker" "php" "artisan queue:listen"
    $processes += Start-DevService "Frontend" "npm" "run dev"

    Write-Host "✅ All services running! Press Ctrl+C to stop all." -ForegroundColor Green
    while ($true) { Start-Sleep -Seconds 1 }
}
finally {
    Write-Host "`n🛑 Shutting down all services cleanly..." -ForegroundColor Red
    foreach ($p in $processes) {
        if ($p -and -not $p.HasExited) {
            Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
        }
    }
    Write-Host "All processes terminated." -ForegroundColor DarkGray
}
```

### 2. WSL / Linux Runner: `scripts/dev.sh`
Must trap `SIGINT` / `SIGTERM` so child background PIDs are killed on exit:
```bash
#!/usr/bin/env bash
set -e

PIDS=()

cleanup() {
    echo -e "\n\033[0;31m🛑 Shutting down all dev services cleanly...\033[0m"
    for pid in "${PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null || true
        fi
    done
    wait 2>/dev/null || true
    echo "All processes terminated."
}

trap cleanup SIGINT SIGTERM EXIT

echo -e "\033[0;36m🚀 Starting Local Dev Stack in WSL/Linux...\033[0m"

# Example processes
php artisan serve --port=8000 & PIDS+=($!)
php artisan reverb:start & PIDS+=($!)
php artisan queue:listen & PIDS+=($!)
npm run dev & PIDS+=($!)

echo -e "\033[0;32m✅ All services running! Press Ctrl+C to stop all.\033[0m"
wait
```

---

## Phase 4: Health Verification & Status Report

Once launched, ping the services to confirm they are actively accepting connections:
* Query `http://127.0.0.1:8000` (Backend API).
* Query `http://127.0.0.1:5173` (Vite / Frontend).
* Verify Reverb WebSocket port (default `8080` or `env(REVERB_PORT)`).

Output a clean status table:
```
Service          Port     Status      Command
────────────────────────────────────────────────────────
Backend API      8000     UP (200 OK) php artisan serve
Reverb WS        8080     UP (Open)   php artisan reverb:start
Queue Worker     -        ACTIVE      php artisan queue:listen
Frontend (Vite)  5173     UP (200 OK) npm run dev
```
