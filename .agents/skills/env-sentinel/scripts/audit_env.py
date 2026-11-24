#!/usr/bin/env python3
"""
audit_env.py — Zero-Drift Secret & Environment Synchronizer
Audits codebases for environment variable drift, secret leaks, and missing configuration keys.
Synchronizes .env and .env.example with zero-drift safety checks.
"""

import os
import sys
import re
import argparse
from pathlib import Path

# Common ignore directories
IGNORE_DIRS = {
    "node_modules", ".git", "venv", ".venv", "dist", "build",
    "vendor", ".next", ".nuxt", "__pycache__", ".cache", ".idea", ".vscode"
}

# Regex patterns for environment variable lookups across languages
PATTERNS = [
    # Node / TypeScript / JS
    r"process\.env\.([A-Z0-9_]{2,})",
    r"process\.env\[['\"]([A-Z0-9_]{2,})['\"]\]",
    # Python
    r"os\.environ\.get\(\s*['\"]([A-Z0-9_]{2,})['\"]",
    r"os\.environ\[\s*['\"]([A-Z0-9_]{2,})['\"]\]",
    r"os\.getenv\(\s*['\"]([A-Z0-9_]{2,})['\"]",
    # PHP / Laravel
    r"env\(\s*['\"]([A-Z0-9_]{2,})['\"]",
    r"getenv\(\s*['\"]([A-Z0-9_]{2,})['\"]",
    r"\$_ENV\[\s*['\"]([A-Z0-9_]{2,})['\"]\]",
    # Go
    r"os\.Getenv\(\s*['\"]([A-Z0-9_]{2,})['\"]",
    # Rust
    r"env::var\(\s*['\"]([A-Z0-9_]{2,})['\"]",
    # Docker Compose / Bash / YAML
    r"\$\{([A-Z0-9_]{2,})(?::-.*?)?\}"
]

# Patterns that suggest live production secrets leaked
SECRET_LEAK_PATTERNS = [
    (r"sk_live_[0-9a-zA-Z]{24,}", "Stripe Live Secret Key"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
    (r"ghp_[0-9a-zA-Z]{36}", "GitHub Personal Access Token"),
    (r"AIza[0-9A-Za-z\\-_]{35}", "Google API Key"),
    (r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----", "Private Cryptographic Key"),
    (r"(?:postgres|mysql|mongodb):\/\/[^:]+:[^@]+@", "Database Connection String with Password")
]

def scan_codebase_for_env_vars(root_dir="."):
    """Scans code files and collects all referenced environment variable keys."""
    root = Path(root_dir)
    detected = {}

    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if any(ignored in p.parts for ignored in IGNORE_DIRS):
            continue
        # Scan typical source files
        if p.suffix in {".ts", ".tsx", ".js", ".jsx", ".py", ".php", ".go", ".rs", ".yml", ".yaml", ".sh", ".ps1"}:
            try:
                content = p.read_text(encoding="utf-8", errors="ignore")
                for pat in PATTERNS:
                    matches = re.findall(pat, content)
                    for key in matches:
                        # Filter out generic noise or JS globals
                        if key in {"NODE_ENV", "PATH", "HOME", "USER", "PWD"}:
                            continue
                        if key not in detected:
                            detected[key] = set()
                        detected[key].add(str(p.relative_to(root).as_posix()))
            except Exception:
                pass

    return detected

def parse_env_file(filepath):
    """Parses key-value pairs from an env file."""
    path = Path(filepath)
    if not path.exists():
        return {}
    keys = {}
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                keys[k] = v
    except Exception:
        pass
    return keys

def scan_for_secret_leaks(root_dir="."):
    """Checks source code and env files for dangerous hardcoded secrets."""
    root = Path(root_dir)
    leaks = []

    for p in root.rglob("*"):
        if p.is_dir() or any(ignored in p.parts for ignored in IGNORE_DIRS):
            continue
        # Check source and configuration files (ignore .env.example)
        if p.name == ".env.example":
            continue
        if p.suffix in {".ts", ".tsx", ".js", ".jsx", ".py", ".json", ".yml", ".yaml", ".env"} or p.name.startswith(".env"):
            try:
                content = p.read_text(encoding="utf-8", errors="ignore")
                for pat, label in SECRET_LEAK_PATTERNS:
                    if re.search(pat, content):
                        leaks.append({"file": str(p.relative_to(root).as_posix()), "type": label})
            except Exception:
                pass

    return leaks

def infer_var_type(var_name):
    """Infers expected type annotation based on variable naming conventions."""
    name = var_name.upper()
    if any(k in name for k in ("PORT", "TIMEOUT", "MAX_", "MIN_", "COUNT", "LIMIT")):
        return "number", "3000"
    if any(k in name for k in ("ENABLE", "DISABLE", "IS_", "HAS_", "DEBUG", "STRICT")):
        return "boolean", "false"
    if any(k in name for k in ("URL", "URI", "HOST", "ENDPOINT")):
        return "url", "http://localhost:8000"
    if any(k in name for k in ("KEY", "SECRET", "TOKEN", "PASSWORD")):
        return "secret", "your-secret-key-here"
    return "string", "default_value"

def sync_env_example(missing_keys, example_path=".env.example"):
    """Appends missing keys to .env.example with safe defaults."""
    path = Path(example_path)
    existing_text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else "# Environment Configuration Template\n"
    
    append_lines = ["\n# --- Added by env-sentinel auto-sync ---"]
    for k in sorted(missing_keys):
        vtype, default_val = infer_var_type(k)
        append_lines.append(f"# Type: {vtype}")
        append_lines.append(f"{k}={default_val}")

    updated = existing_text.rstrip() + "\n" + "\n".join(append_lines) + "\n"
    path.write_text(updated, encoding="utf-8")
    return path

def main():
    parser = argparse.ArgumentParser(description="Zero-Drift Secret & Environment Synchronizer")
    parser.add_argument("--dir", default=".", help="Root directory of the project")
    parser.add_argument("--env", default=".env", help="Path to local .env file")
    parser.add_argument("--example", default=".env.example", help="Path to .env.example file")
    parser.add_argument("--sync", action="store_true", help="Auto-sync missing keys to .env.example with safe stubs")
    parser.add_argument("--strict", action="store_true", help="Exit with non-zero code if any drifts or leaks exist")

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print(" 🛡️ ENV SENTINEL: AUDIT REPORT")
    print("=" * 60)

    # 1. Collect vars from source code
    code_vars = scan_codebase_for_env_vars(args.dir)
    print(f"  • Source Code References : {len(code_vars)} unique env keys")

    # 2. Parse env files
    local_env = parse_env_file(Path(args.dir) / args.env)
    example_env = parse_env_file(Path(args.dir) / args.example)

    print(f"  • Keys in {args.example:<15} : {len(example_env)} keys")
    print(f"  • Keys in {args.env:<15} : {len(local_env)} keys")

    # 3. Detect Drifts
    code_keys = set(code_vars.keys())
    example_keys = set(example_env.keys())
    local_keys = set(local_env.keys())

    missing_in_example = code_keys - example_keys
    missing_in_local = example_keys - local_keys
    orphaned_in_example = example_keys - code_keys

    # 4. Check Secret Leaks
    leaks = scan_for_secret_leaks(args.dir)

    # Render Report
    has_issues = False

    if leaks:
        has_issues = True
        print("\n🚨 CRITICAL: POTENTIAL SECRET LEAKS DETECTED:")
        for l in leaks:
            print(f"  [!] {l['file']} -> {l['type']}")

    if missing_in_example:
        has_issues = True
        print(f"\n⚠️  MISSING IN {args.example} ({len(missing_in_example)} keys used in code):")
        for k in sorted(missing_in_example):
            locs = ", ".join(list(code_vars[k])[:2])
            print(f"  [-] {k:<25} (referenced in: {locs})")

    if missing_in_local:
        print(f"\nℹ️  DECLARED IN EXAMPLE BUT MISSING IN LOCAL {args.env} ({len(missing_in_local)} keys):")
        for k in sorted(missing_in_local):
            print(f"  [?] {k}")

    if orphaned_in_example:
        print(f"\n🧹 ORPHANED IN {args.example} ({len(orphaned_in_example)} keys not found in code):")
        for k in sorted(orphaned_in_example):
            print(f"  [~] {k}")

    if not has_issues and not missing_in_local and not orphaned_in_example:
        print("\n✅ Zero drift detected. Environment configurations are perfectly synchronized!")

    # Auto-sync action
    if args.sync and missing_in_example:
        synced_file = sync_env_example(missing_in_example, Path(args.dir) / args.example)
        print(f"\n[env-sentinel] Successfully synchronized {len(missing_in_example)} missing keys to {synced_file.resolve()}")

    print("=" * 60)

    if args.strict and has_issues:
        sys.exit(1)

if __name__ == "__main__":
    main()
