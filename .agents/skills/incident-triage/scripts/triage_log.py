#!/usr/bin/env python3
"""
triage_log.py — Real-Time Crash & Log Forensic Triager
Parses stack traces, extracts culprit lines, runs git blame, and scaffolds minimal repros for /hub.
"""

import os
import sys
import re
import argparse
import subprocess
from pathlib import Path

def parse_stack_trace(raw_text):
    """Detects runtime stack traces across Node/TS, Python, PHP, Rust, and Go."""
    forensics = {
        "runtime": "Unknown",
        "error_type": "Unknown Error",
        "error_message": "",
        "culprit_file": None,
        "culprit_line": None,
        "culprit_col": None,
        "full_trace": raw_text.strip()
    }

    # 1. Python Stack Trace
    # Traceback (most recent call last): ... File "foo.py", line 42, in bar ... Error: msg
    if "Traceback (most recent call last):" in raw_text:
        forensics["runtime"] = "Python"
        py_files = re.findall(r'File "([^"]+)", line (\d+)(?:, in (\w+))?', raw_text)
        if py_files:
            # Take the last application file (closest to crash)
            forensics["culprit_file"] = py_files[-1][0]
            forensics["culprit_line"] = int(py_files[-1][1])
        # Find final error line
        err_match = re.search(r'([A-Za-z0-9_]+Error|[A-Za-z0-9_]+Exception):\s*(.*)', raw_text)
        if err_match:
            forensics["error_type"] = err_match.group(1)
            forensics["error_message"] = err_match.group(2)

    # 2. Node.js / TypeScript Stack Trace
    # Error: message \n at function (/path/file.ts:42:10)
    elif re.search(r'(?:(?:TypeError|ReferenceError|SyntaxError|Error|Exception):\s*.*|\bat\s+.*:\d+:\d+)', raw_text):
        forensics["runtime"] = "Node.js / TypeScript"
        err_header = re.search(r'([A-Za-z0-9_$]+Error):\s*(.*)', raw_text)
        if err_header:
            forensics["error_type"] = err_header.group(1)
            forensics["error_message"] = err_header.group(2)
        
        frames = re.findall(r'at\s+(?:.*?\s+\()?([^\s()]+):(\d+):(\d+)\)?', raw_text)
        for path, line, col in frames:
            # Prefer non-node_modules frames
            if "node_modules" not in path and not path.startswith("internal/"):
                forensics["culprit_file"] = path
                forensics["culprit_line"] = int(line)
                forensics["culprit_col"] = int(col)
                break
        if not forensics["culprit_file"] and frames:
            forensics["culprit_file"] = frames[0][0]
            forensics["culprit_line"] = int(frames[0][1])
            forensics["culprit_col"] = int(frames[0][2])

    # 3. Rust panic
    # thread 'main' panicked at 'message', src/main.rs:15:9
    elif "panicked at" in raw_text:
        forensics["runtime"] = "Rust"
        rust_match = re.search(r"panicked at\s*['\"]([^'\"]+)['\"],\s*([^\s:]+):(\d+):(\d+)", raw_text)
        if rust_match:
            forensics["error_type"] = "Panic"
            forensics["error_message"] = rust_match.group(1)
            forensics["culprit_file"] = rust_match.group(2)
            forensics["culprit_line"] = int(rust_match.group(3))
            forensics["culprit_col"] = int(rust_match.group(4))

    # 4. PHP / Laravel
    # Fatal error: Uncaught Exception: msg in /path/file.php:42
    elif "Fatal error:" in raw_text or "production.ERROR:" in raw_text:
        forensics["runtime"] = "PHP / Laravel"
        php_match = re.search(r'(?:Fatal error:\s*Uncaught\s*|production\.ERROR:\s*)([A-Za-z0-9_\\]+):\s*(.*?)(?:\s*in\s*|\s*\{)(.*?):(\d+)', raw_text)
        if php_match:
            forensics["error_type"] = php_match.group(1)
            forensics["error_message"] = php_match.group(2)
            forensics["culprit_file"] = php_match.group(3)
            forensics["culprit_line"] = int(php_match.group(4))

    # Generic fallback
    if not forensics["culprit_file"]:
        generic_match = re.search(r'([A-Za-z0-9_./\\-]+\.[a-z]{2,4}):(\d+)', raw_text)
        if generic_match:
            forensics["culprit_file"] = generic_match.group(1)
            forensics["culprit_line"] = int(generic_match.group(2))

    return forensics

def get_code_context(file_path, line_no, window=3):
    """Reads surrounding source code lines around culprit line."""
    p = Path(file_path)
    if not p.exists() or not p.is_file():
        return None
    try:
        lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
        start = max(0, line_no - window - 1)
        end = min(len(lines), line_no + window)
        result = []
        for idx in range(start, end):
            curr_line = idx + 1
            marker = ">>" if curr_line == line_no else "  "
            result.append(f"{marker} {curr_line:4d} | {lines[idx]}")
        return "\n".join(result)
    except Exception:
        return None

def get_git_blame(file_path, line_no):
    """Queries git blame for the specific line."""
    p = Path(file_path)
    if not p.exists():
        return None
    try:
        cmd = ["git", "blame", "-L", f"{line_no},{line_no}", "--porcelain", str(p)]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = res.stdout.splitlines()
        if not lines:
            return None
        commit_hash = lines[0].split()[0]
        author = "Unknown"
        summary = ""
        for line in lines:
            if line.startswith("author "):
                author = line[7:]
            elif line.startswith("summary "):
                summary = line[8:]
        return {
            "commit": commit_hash[:8],
            "author": author,
            "summary": summary
        }
    except Exception:
        return None

def scaffold_repro_stub(forensics, out_file):
    """Scaffolds a minimal reproduction test file."""
    runtime = forensics["runtime"]
    p = Path(out_file)
    p.parent.mkdir(parents=True, exist_ok=True)

    if runtime.startswith("Python") or str(out_file).endswith(".py"):
        content = f'''"""
repro_test.py — Minimal Failing Reproduction Test
Root Cause Target: {forensics["error_type"]} ({forensics["error_message"]})
Culprit: {forensics["culprit_file"]}:{forensics["culprit_line"]}
"""

import pytest

def test_reproduce_incident():
    # 1. Arrange: Minimal failing payload
    # TODO: Supply input that triggers {forensics["error_type"]}
    
    # 2. Act & Assert: This test MUST fail before fix is applied
    with pytest.raises(Exception):
        # Call the offending function from {forensics["culprit_file"]}
        pass
'''
    else:
        content = f'''/**
 * repro.test.ts — Minimal Failing Reproduction Test
 * Root Cause Target: {forensics["error_type"]} ({forensics["error_message"]})
 * Culprit: {forensics["culprit_file"]}:{forensics["culprit_line"]}
 */

import {{ describe, it, expect }} from "vitest";

describe("Incident Reproduction: {forensics["error_type"]}", () => {{
  it("reproduces the failure under boundary condition", async () => {{
    // 1. Arrange: Input causing the crash
    // TODO: Add input parameters

    // 2. Act & Assert: Expect function to fail or trigger error
    expect(() => {{
      // Offending call
    }}).toThrow();
  }});
}});
'''
    p.write_text(content, encoding="utf-8")
    return p

def main():
    parser = argparse.ArgumentParser(description="Real-Time Crash & Log Forensic Triager")
    parser.add_argument("target", nargs="?", default="-", help="Log file path, or '-' to read from stdin")
    parser.add_argument("--text", help="Raw error string passed directly")
    parser.add_argument("--out-repro", help="Optional path to scaffold a minimal reproduction test file")

    args = parser.parse_args()

    # Read input
    if args.text:
        raw_log = args.text
    elif args.target == "-":
        if sys.stdin.isatty():
            print("[incident-triage] Enter or paste stack trace (Press Ctrl+Z or Ctrl+D on blank line to finish):")
        raw_log = sys.stdin.read()
    else:
        log_path = Path(args.target)
        if not log_path.exists():
            print(f"[incident-triage] Error: File '{args.target}' does not exist.")
            sys.exit(1)
        raw_log = log_path.read_text(encoding="utf-8", errors="ignore")

    if not raw_log.strip():
        print("[incident-triage] No log content provided.")
        sys.exit(0)

    forensics = parse_stack_trace(raw_log)

    print("\n" + "=" * 60)
    print(" 🚨 INCIDENT FORENSIC REPORT")
    print("=" * 60)
    print(f"  • Runtime Engine : {forensics['runtime']}")
    print(f"  • Error Type     : {forensics['error_type']}")
    print(f"  • Message        : {forensics['error_message'] or '(none detected)'}")
    print(f"  • Culprit File   : {forensics['culprit_file'] or '(unresolved)'}")
    print(f"  • Line / Column  : {forensics['culprit_line'] or 'N/A'}:{forensics['culprit_col'] or 'N/A'}")

    # Code Context
    if forensics["culprit_file"] and forensics["culprit_line"]:
        context = get_code_context(forensics["culprit_file"], forensics["culprit_line"])
        if context:
            print("\n🔍 SOURCE CODE CONTEXT:")
            print(context)

        # Git Blame
        blame = get_git_blame(forensics["culprit_file"], forensics["culprit_line"])
        if blame:
            print("\n👤 GIT BLAME INTEL:")
            print(f"  • Commit  : {blame['commit']}")
            print(f"  • Author  : {blame['author']}")
            print(f"  • Summary : {blame['summary']}")

    # Hub Dispatch Command
    culprit_str = f"{forensics['culprit_file']}:{forensics['culprit_line']}" if forensics['culprit_file'] else "unknown file"
    err_str = f"{forensics['error_type']}: {forensics['error_message']}".strip(": ")
    hub_cmd = f"/hub {err_str} in {culprit_str}. repro first, then fix and verify."

    print("\n" + "-" * 60)
    print(" 🎯 RECOMMENDED HUB DISPATCH (Level 2 Bug-Fix):")
    print(f"  {hub_cmd}")
    print("-" * 60)

    # Scaffolding repro stub
    if args.out_repro:
        out_path = scaffold_repro_stub(forensics, args.out_repro)
        print(f"\n[incident-triage] Minimal reproduction stub written to: {out_path.resolve()}")

if __name__ == "__main__":
    main()
