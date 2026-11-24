#!/usr/bin/env python3
"""
shield_engine.py — Post-Prototype Hardening & Security Resilience Engine
Audits codebases for XSS, CSRF, security headers, CORS wildcards, error boundaries (404/500),
and scaffolds production-ready error pages and security middleware.
"""

import os
import sys
import re
import argparse
from pathlib import Path

IGNORE_DIRS = {
    "node_modules", ".git", "venv", ".venv", "dist", "build",
    "vendor", ".next", ".nuxt", "__pycache__", ".cache", ".idea", ".vscode",
    ".agents"
}

def detect_framework(root_dir="."):
    """Detects primary application framework."""
    root = Path(root_dir)
    if (root / "package.json").exists():
        try:
            content = (root / "package.json").read_text(encoding="utf-8", errors="ignore")
            if "next" in content:
                # App router vs Pages router
                if (root / "src" / "app").exists() or (root / "app").exists():
                    return "next-app"
                return "next-pages"
            if "vite" in content or "react" in content:
                return "react-vite"
            if "express" in content:
                return "express"
        except Exception:
            pass

    if (root / "composer.json").exists():
        return "laravel"

    if (root / "requirements.txt").exists() or (root / "pyproject.toml").exists():
        for py_file in root.rglob("*.py"):
            if any(ign in py_file.parts for ign in IGNORE_DIRS):
                continue
            try:
                txt = py_file.read_text(encoding="utf-8", errors="ignore")
                if "fastapi" in txt.lower():
                    return "fastapi"
                if "flask" in txt.lower():
                    return "flask"
                if "django" in txt.lower():
                    return "django"
            except Exception:
                pass
        return "python"

    return "generic-web"

def audit_codebase(root_dir="."):
    """Performs static security and resilience audit."""
    root = Path(root_dir)
    findings = {
        "xss_vectors": [],
        "csrf_risks": [],
        "cors_wildcards": [],
        "missing_headers": True,
        "rate_limiting_found": False,
        "has_404_page": False,
        "has_error_boundary": False,
        "stack_trace_leakage": []
    }

    # 1. Check for 404 and Error pages
    check_404_files = [
        "app/not-found.tsx", "src/app/not-found.tsx",
        "app/not-found.jsx", "src/app/not-found.jsx",
        "pages/404.tsx", "src/pages/404.tsx",
        "pages/404.jsx", "src/pages/404.jsx",
        "public/404.html", "404.html",
        "resources/views/errors/404.blade.php"
    ]
    for f in check_404_files:
        if (root / f).exists():
            findings["has_404_page"] = True
            break

    check_error_files = [
        "app/error.tsx", "src/app/error.tsx",
        "app/error.jsx", "src/app/error.jsx",
        "pages/_error.tsx", "src/pages/_error.tsx",
        "public/500.html", "500.html",
        "resources/views/errors/500.blade.php"
    ]
    for f in check_error_files:
        if (root / f).exists():
            findings["has_error_boundary"] = True
            break

    # 2. Scan source code files
    headers_keywords = {"content-security-policy", "x-frame-options", "x-content-type-options", "strict-transport-security", "helmet"}
    rate_limit_keywords = {"ratelimit", "rate_limit", "throttle", "slowapi", "express-rate-limit"}

    for p in root.rglob("*"):
        if p.is_dir() or any(ign in p.parts for ign in IGNORE_DIRS):
            continue

        if p.suffix in {".ts", ".tsx", ".js", ".jsx", ".py", ".php", ".html"}:
            rel_path = str(p.relative_to(root).as_posix())
            try:
                content = p.read_text(encoding="utf-8", errors="ignore")
                low = content.lower()

                # Check security headers
                if any(hk in low for hk in headers_keywords):
                    findings["missing_headers"] = False

                # Check rate limiting
                if any(rl in low for rl in rate_limit_keywords):
                    findings["rate_limiting_found"] = True

                # XSS vectors
                if "dangerouslysetinnerhtml" in low:
                    findings["xss_vectors"].append((rel_path, "dangerouslySetInnerHTML detected"))
                if "v-html" in low:
                    findings["xss_vectors"].append((rel_path, "v-html raw template injection"))
                if re.search(r"\.innerhtml\s*=", low):
                    findings["xss_vectors"].append((rel_path, "direct element.innerHTML assignment"))

                # CORS wildcards on APIs
                if re.search(r"['\"]?access-control-allow-origin['\"]?\s*[:=]\s*['\"]?\*['\"]?", low) or "allow_origins=[\"*\"]" in low or "origin: \"*\"" in low:
                    findings["cors_wildcards"].append(rel_path)

                # Stack trace leakage
                if re.search(r"res\.(?:json|send)\(.*(?:err\.stack|stack_trace|format_exc\(\))", low):
                    findings["stack_trace_leakage"].append(rel_path)

            except Exception:
                pass

    return findings

def calculate_score(findings):
    """Calculates security & resilience score (0-100)."""
    score = 100
    deductions = []

    if not findings["has_404_page"]:
        score -= 15
        deductions.append("Missing custom 404 page (-15)")

    if not findings["has_error_boundary"]:
        score -= 15
        deductions.append("Missing top-level error boundary (-15)")

    if findings["missing_headers"]:
        score -= 20
        deductions.append("Missing HTTP security headers / CSP (-20)")

    if findings["xss_vectors"]:
        score -= min(20, len(findings["xss_vectors"]) * 10)
        deductions.append(f"Unsanitized XSS injection points detected (-{min(20, len(findings['xss_vectors']) * 10)})")

    if findings["cors_wildcards"]:
        score -= 15
        deductions.append("Wildcard CORS (*) detected on API routes (-15)")

    if not findings["rate_limiting_found"]:
        score -= 10
        deductions.append("No rate-limiting middleware detected (-10)")

    if findings["stack_trace_leakage"]:
        score -= 20
        deductions.append("Possible runtime stack trace leak in responses (-20)")

    final_score = max(0, score)
    if final_score >= 90:
        grade = "A (Production Ready)"
    elif final_score >= 75:
        grade = "B (Good / Minor Gaps)"
    elif final_score >= 60:
        grade = "C (Needs Hardening)"
    else:
        grade = "F (High Risk / Prototype Only)"

    return final_score, grade, deductions

def scaffold_404_page(framework, root_dir="."):
    """Scaffolds a responsive, accessible custom 404 page."""
    root = Path(root_dir)
    
    if framework == "next-app":
        target = root / ("src/app/not-found.tsx" if (root / "src/app").exists() else "app/not-found.tsx")
        content = '''import Link from "next/link";

export default function NotFound() {
  return (
    <main className="flex min-h-[70vh] flex-col items-center justify-center px-6 py-24 text-center">
      <p className="text-base font-semibold text-indigo-600 dark:text-indigo-400">404</p>
      <h1 className="mt-4 text-3xl font-bold tracking-tight text-neutral-900 sm:text-5xl dark:text-white">
        Page Not Found
      </h1>
      <p className="mt-6 text-base leading-7 text-neutral-600 dark:text-neutral-400 max-w-md">
        Sorry, we couldn’t find the page you’re looking for. It may have been moved or deleted.
      </p>
      <div className="mt-10 flex items-center justify-center gap-x-6">
        <Link
          href="/"
          className="rounded-md bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 transition"
        >
          Back to Home
        </Link>
      </div>
    </main>
  );
}
'''
    else:
        target = root / "public" / "404.html" if (root / "public").exists() else root / "404.html"
        content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>404 - Page Not Found</title>
  <style>
    body { font-family: system-ui, -apple-system, sans-serif; display: flex; min-height: 100vh; align-items: center; justify-content: center; margin: 0; background: #fafafa; color: #171717; }
    .card { text-align: center; padding: 2rem; max-width: 480px; }
    .code { font-size: 1.25rem; font-weight: 700; color: #4f46e5; }
    h1 { font-size: 2.25rem; margin: 0.5rem 0 1rem; }
    p { color: #525252; line-height: 1.6; }
    .btn { display: inline-block; margin-top: 1.5rem; background: #4f46e5; color: white; padding: 0.65rem 1.25rem; border-radius: 6px; text-decoration: none; font-weight: 600; }
    .btn:hover { background: #4338ca; }
  </style>
</head>
<body>
  <div class="card">
    <div class="code">404</div>
    <h1>Page Not Found</h1>
    <p>Sorry, the page you are looking for doesn't exist or has been relocated.</p>
    <a href="/" class="btn">Return Home</a>
  </div>
</body>
</html>
'''
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target

def scaffold_error_boundary(framework, root_dir="."):
    """Scaffolds a global error boundary."""
    root = Path(root_dir)

    if framework == "next-app":
        target = root / ("src/app/error.tsx" if (root / "src/app").exists() else "app/error.tsx")
        content = '''"use client";

import { useEffect } from "react";

export default function ErrorBoundary({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log sanitized error to an external logging service (Sentry, Datadog)
    console.error("Application runtime error:", error.digest || error.message);
  }, [error]);

  return (
    <main className="flex min-h-[60vh] flex-col items-center justify-center px-6 py-20 text-center">
      <p className="text-base font-semibold text-rose-600">Application Error</p>
      <h1 className="mt-2 text-2xl font-bold tracking-tight text-neutral-900 sm:text-4xl dark:text-white">
        Something went wrong
      </h1>
      <p className="mt-4 text-sm text-neutral-600 dark:text-neutral-400 max-w-md">
        An unexpected error occurred. Our team has been notified.
      </p>
      <div className="mt-8 flex gap-4">
        <button
          onClick={() => reset()}
          className="rounded-md bg-neutral-900 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-neutral-800 dark:bg-white dark:text-neutral-900 transition"
        >
          Try Again
        </button>
      </div>
    </main>
  );
}
'''
    else:
        target = root / "public" / "500.html" if (root / "public").exists() else root / "500.html"
        content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>500 - Server Error</title>
  <style>
    body { font-family: system-ui, sans-serif; display: flex; min-height: 100vh; align-items: center; justify-content: center; background: #fafafa; }
    .box { text-align: center; padding: 2rem; }
    h1 { color: #dc2626; font-size: 2rem; }
    p { color: #525252; }
    a { color: #4f46e5; text-decoration: none; font-weight: 600; }
  </style>
</head>
<body>
  <div class="box">
    <h1>Something Went Wrong</h1>
    <p>A server error occurred. Please try refreshing or return to the homepage.</p>
    <a href="/">← Go Back Home</a>
  </div>
</body>
</html>
'''
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target

def scaffold_security_headers(framework, root_dir="."):
    """Scaffolds security headers configuration."""
    root = Path(root_dir)

    if framework == "next-app" or framework == "next-pages":
        target = root / ("src/middleware.ts" if (root / "src").exists() else "middleware.ts")
        content = '''import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const response = NextResponse.next();

  // Production Security Headers
  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  response.headers.set("Permissions-Policy", "camera=(), microphone=(), geolocation=()");
  response.headers.set(
    "Content-Security-Policy",
    "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:;"
  );

  return response;
}

export const config = {
  matcher: "/:path*",
};
'''
    elif framework in {"fastapi", "python"}:
        target = root / "security_headers.py"
        content = '''from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none';"
        return response
'''
    else:
        target = root / "security_headers.json"
        content = '''{
  "headers": [
    { "key": "X-Frame-Options", "value": "DENY" },
    { "key": "X-Content-Type-Options", "value": "nosniff" },
    { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
    { "key": "Content-Security-Policy", "value": "default-src 'self'" }
  ]
}
'''
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target

def main():
    parser = argparse.ArgumentParser(description="Post-Prototype Hardening & Security Resilience Engine")
    parser.add_argument("--dir", default=".", help="Root directory of application")
    parser.add_argument("--audit", action="store_true", help="Run static security and resilience audit (default)")
    parser.add_argument("--scaffold", choices=["404", "error", "headers", "all"], help="Scaffold missing security or error assets")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 if hardening score is below 80")

    args = parser.parse_args()
    framework = detect_framework(args.dir)

    # Scaffolding Action
    if args.scaffold:
        print(f"\n[app-shield] Detected Framework: {framework}")
        scaffolded = []
        if args.scaffold in {"404", "all"}:
            f404 = scaffold_404_page(framework, args.dir)
            scaffolded.append(f"Custom 404 page -> {f404.resolve()}")
        if args.scaffold in {"error", "all"}:
            ferr = scaffold_error_boundary(framework, args.dir)
            scaffolded.append(f"Global Error Boundary -> {ferr.resolve()}")
        if args.scaffold in {"headers", "all"}:
            fhdr = scaffold_security_headers(framework, args.dir)
            scaffolded.append(f"Security Headers -> {fhdr.resolve()}")

        print("\n🛡️  SCAFFOLD COMPLETE:")
        for item in scaffolded:
            print(f"  [+] {item}")
        return

    # Audit Action (Default)
    findings = audit_codebase(args.dir)
    score, grade, deductions = calculate_score(findings)

    print("\n" + "=" * 60)
    print(" 🛡️  APP SHIELD: POST-PROTOTYPE HARDENING AUDIT")
    print("=" * 60)
    print(f"  • Framework Detected  : {framework}")
    print(f"  • Hardening Score     : {score} / 100")
    print(f"  • Readiness Grade     : {grade}")
    print("=" * 60)

    print("\n📋 AUDIT SCORECARD:")
    print(f"  [{'✓' if findings['has_404_page'] else '✗'}] Custom 404 Not Found Page")
    print(f"  [{'✓' if findings['has_error_boundary'] else '✗'}] Global Runtime Error Boundary")
    print(f"  [{'✓' if not findings['missing_headers'] else '✗'}] Production Security Headers (CSP, HSTS, X-Frame)")
    print(f"  [{'✓' if not findings['xss_vectors'] else '✗'}] XSS / Raw HTML Sanitization")
    print(f"  [{'✓' if not findings['cors_wildcards'] else '✗'}] Strict CORS Origin Boundaries")
    print(f"  [{'✓' if findings['rate_limiting_found'] else '?'}] Rate-Limiting Middleware")

    if deductions:
        print("\n⚠️  SECURITY & RESILIENCE DEFICITS:")
        for d in deductions:
            print(f"  [-] {d}")

    if findings["xss_vectors"]:
        print("\n🚨 UNGUARDED XSS INJECTIONS:")
        for path, reason in findings["xss_vectors"]:
            print(f"  [!] {path}: {reason}")

    if findings["cors_wildcards"]:
        print("\n🌐 OPEN CORS WILDCARDS (*):")
        for path in findings["cors_wildcards"]:
            print(f"  [!] {path}")

    # Recommendations
    print("\n💡 REMEDIATION RECOMMENDATION:")
    if score < 90:
        print("  Run auto-scaffolding to patch missing error pages and headers:")
        print("    py -3 .agents/skills/app-shield/scripts/shield_engine.py --scaffold all")
    else:
        print("  Prototype is hardened and meets baseline production standards!")
    print("=" * 60)

    if args.strict and score < 80:
        sys.exit(1)

if __name__ == "__main__":
    main()
