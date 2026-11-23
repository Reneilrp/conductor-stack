#!/usr/bin/env python3
"""
detect_stack.py - Intelligently audits a repository's codebase and outputs a canonical ARCHITECTURE.md manifesto.
"""

import sys
import os
import json
from pathlib import Path

def audit_directory(root_dir="."):
    root = Path(root_dir).resolve()
    manifest = {
        "project_name": root.name,
        "frontend": {"framework": None, "styling": None, "state": None, "tools": []},
        "backend": {"language": None, "framework": None, "api_type": None, "tools": []},
        "database": {"orm": None, "engine": None, "cache_queue": None},
        "architecture": {"type": "Standard Monolith", "key_directories": [], "patterns": []},
        "dev_environment": {"package_manager": None, "test_runner": None, "services": []}
    }

    # 1. Inspect package.json (Node/JS/TS)
    pkg_file = root / "package.json"
    if pkg_file.exists():
        try:
            with open(pkg_file, "r", encoding="utf-8") as f:
                pkg = json.load(f)
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            
            # Frameworks
            if "next" in deps: manifest["frontend"]["framework"] = f"Next.js ({deps['next']})"
            elif "react" in deps: manifest["frontend"]["framework"] = f"React ({deps['react']})"
            elif "vue" in deps: manifest["frontend"]["framework"] = f"Vue ({deps['vue']})"
            elif "nuxt" in deps: manifest["frontend"]["framework"] = f"Nuxt ({deps['nuxt']})"
            elif "svelte" in deps: manifest["frontend"]["framework"] = f"Svelte ({deps['svelte']})"
            
            # Styling
            if "tailwindcss" in deps: manifest["frontend"]["styling"] = "Tailwind CSS"
            elif "@chakra-ui/react" in deps: manifest["frontend"]["styling"] = "Chakra UI"
            elif "@mui/material" in deps: manifest["frontend"]["styling"] = "Material UI"
            
            # State
            if "zustand" in deps: manifest["frontend"]["state"] = "Zustand"
            elif "@reduxjs/toolkit" in deps: manifest["frontend"]["state"] = "Redux Toolkit"
            elif "pinia" in deps: manifest["frontend"]["state"] = "Pinia"
            elif "@tanstack/react-query" in deps: manifest["frontend"]["tools"].append("TanStack Query")
            
            # Backend in Node
            if "@nestjs/core" in deps:
                manifest["backend"]["language"] = "TypeScript/Node"
                manifest["backend"]["framework"] = "NestJS"
            elif "express" in deps:
                manifest["backend"]["language"] = "JavaScript/Node"
                manifest["backend"]["framework"] = "Express"
            elif "hono" in deps:
                manifest["backend"]["language"] = "TypeScript/Node"
                manifest["backend"]["framework"] = "Hono"
                
            # ORMs
            if "prisma" in deps or "@prisma/client" in deps: manifest["database"]["orm"] = "Prisma"
            elif "drizzle-orm" in deps: manifest["database"]["orm"] = "Drizzle"
            elif "typeorm" in deps: manifest["database"]["orm"] = "TypeORM"
            elif "mongoose" in deps: manifest["database"]["orm"] = "Mongoose (MongoDB)"

            # Test runners
            if "vitest" in deps: manifest["dev_environment"]["test_runner"] = "Vitest"
            elif "jest" in deps: manifest["dev_environment"]["test_runner"] = "Jest"
            if "playwright" in deps or "@playwright/test" in deps: manifest["dev_environment"]["tools"] = "Playwright"
        except Exception:
            pass

    # 2. Inspect composer.json (PHP / Laravel)
    composer_file = root / "composer.json"
    if composer_file.exists():
        manifest["backend"]["language"] = "PHP"
        try:
            with open(composer_file, "r", encoding="utf-8") as f:
                comp = json.load(f)
            cdeps = {**comp.get("require", {}), **comp.get("require-dev", {})}
            if "laravel/framework" in cdeps:
                manifest["backend"]["framework"] = f"Laravel ({cdeps['laravel/framework']})"
                manifest["database"]["orm"] = "Eloquent ORM"
            if "laravel/reverb" in cdeps:
                manifest["dev_environment"]["services"].append("Laravel Reverb (WebSockets)")
            if "pestphp/pest" in cdeps: manifest["dev_environment"]["test_runner"] = "Pest"
            elif "phpunit/phpunit" in cdeps: manifest["dev_environment"]["test_runner"] = "PHPUnit"
        except Exception:
            manifest["backend"]["framework"] = "PHP / Custom"

    # 3. Inspect Python (FastAPI, Django, Flask)
    pyproject = root / "pyproject.toml"
    reqs = root / "requirements.txt"
    if pyproject.exists() or reqs.exists() or any(root.glob("*.py")):
        manifest["backend"]["language"] = "Python"
        content = ""
        if reqs.exists(): content += reqs.read_text(encoding="utf-8", errors="ignore")
        if pyproject.exists(): content += pyproject.read_text(encoding="utf-8", errors="ignore")
        
        if "fastapi" in content.lower(): manifest["backend"]["framework"] = "FastAPI"
        elif "django" in content.lower(): manifest["backend"]["framework"] = "Django"
        elif "flask" in content.lower(): manifest["backend"]["framework"] = "Flask"
        if "sqlalchemy" in content.lower(): manifest["database"]["orm"] = "SQLAlchemy"
        if "celery" in content.lower(): manifest["dev_environment"]["services"].append("Celery (Worker)")

    # 4. Check Database Schemas
    if (root / "prisma" / "schema.prisma").exists():
        manifest["database"]["orm"] = "Prisma"
        schema_text = (root / "prisma" / "schema.prisma").read_text(encoding="utf-8", errors="ignore")
        if "postgresql" in schema_text: manifest["database"]["engine"] = "PostgreSQL"
        elif "mysql" in schema_text: manifest["database"]["engine"] = "MySQL"
        elif "sqlite" in schema_text: manifest["database"]["engine"] = "SQLite"

    # 5. Check Package Managers
    if (root / "pnpm-lock.yaml").exists(): manifest["dev_environment"]["package_manager"] = "pnpm"
    elif (root / "yarn.lock").exists(): manifest["dev_environment"]["package_manager"] = "yarn"
    elif (root / "package-lock.json").exists(): manifest["dev_environment"]["package_manager"] = "npm"
    elif (root / "bun.lockb").exists() or (root / "bun.lock").exists(): manifest["dev_environment"]["package_manager"] = "bun"

    # 6. Map Directories
    key_dirs = []
    for d in ["src", "app", "pages", "components", "features", "routes", "controllers", "services", "models", "public"]:
        if (root / d).is_dir():
            key_dirs.append(f"`{d}/`")
    manifest["architecture"]["key_directories"] = key_dirs

    # Monorepo check
    if (root / "pnpm-workspace.yaml").exists() or (root / "turbo.json").exists() or (root / "packages").is_dir():
        manifest["architecture"]["type"] = "Monorepo (Workspaces)"

    return manifest

def generate_markdown(manifest, output_path):
    lines = [
        f"# Project Architecture & Tech Stack: {manifest['project_name']}",
        "",
        "> **Notice for Coding Agents:** This file is the authoritative architectural blueprint for this codebase. Before proposing, adding, or modifying features, adhere to the technologies, patterns, and boundaries declared below.",
        "",
        "---",
        "",
        "## 1. Core Technology Stack",
        "",
        "| Layer | Technology | Details |",
        "|---|---|---|",
        f"| **Frontend** | {manifest['frontend']['framework'] or 'None / Static'} | Styling: {manifest['frontend']['styling'] or 'Standard/CSS'} · State: {manifest['frontend']['state'] or 'None'} |",
        f"| **Backend** | {manifest['backend']['framework'] or manifest['backend']['language'] or 'None / Serverless'} | Language: {manifest['backend']['language'] or 'N/A'} |",
        f"| **Database & ORM** | {manifest['database']['engine'] or 'TBD'} | ORM: {manifest['database']['orm'] or 'None / Raw SQL'} |",
        f"| **Dev Tooling** | Package Mgr: {manifest['dev_environment']['package_manager'] or 'N/A'} | Test Runner: {manifest['dev_environment']['test_runner'] or 'None detected'} |",
        "",
        "---",
        "",
        "## 2. Architecture & Directory Boundaries",
        f"- **Project Type:** {manifest['architecture']['type']}",
        f"- **Discovered Key Folders:** {', '.join(manifest['architecture']['key_directories']) if manifest['architecture']['key_directories'] else 'Flat / Root structure'}",
        "",
        "---",
        "",
        "## 3. Background Services & Daemons",
    ]
    
    if manifest["dev_environment"]["services"]:
        for s in manifest["dev_environment"]["services"]:
            lines.append(f"- {s}")
    else:
        lines.append("- No dedicated background worker daemons detected.")
        
    lines.extend([
        "",
        "---",
        "",
        "## 4. Architectural Rules for Autonomous Agents",
        "1. **Never introduce conflicting runtimes:** Use the established ORM and frameworks listed above.",
        "2. **Honor boundary partitions:** Place shared logic in `src/shared/` or common service directories.",
        "3. **Respect directory layout:** Do not invent alternative module folders when canonical ones exist above."
    ])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ Generated canonical architecture manifesto: {output_path}")

def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    output_file = sys.argv[2] if len(sys.argv) > 2 else os.path.join(target_dir, "ARCHITECTURE.md")
    manifest = audit_directory(target_dir)
    generate_markdown(manifest, output_file)

if __name__ == "__main__":
    main()
