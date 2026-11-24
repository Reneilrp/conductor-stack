#!/usr/bin/env python3
"""
vault_cli.py — Persistent Agent Memory & Decision Log / ADR Manager
Records tooling quirks, architectural decisions, and post-mortem lessons so agents never repeat past mistakes.
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

DEFAULT_VAULT_PATH = Path(".agents/memory/vault.json")

def load_vault(vault_path=DEFAULT_VAULT_PATH):
    """Loads vault database from disk."""
    p = Path(vault_path)
    if not p.exists():
        return {"version": 1, "entries": []}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {"version": 1, "entries": []}

def save_vault(data, vault_path=DEFAULT_VAULT_PATH):
    """Saves vault database to disk."""
    p = Path(vault_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def record_entry(title, category, content, tags=None, vault_path=DEFAULT_VAULT_PATH):
    """Appends a new memory entry."""
    data = load_vault(vault_path)
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry_id = f"{category[:3]}-{len(data['entries']) + 1:03d}"

    entry = {
        "id": entry_id,
        "date": today,
        "category": category, # 'adr', 'quirk', 'lesson'
        "title": title.strip(),
        "tags": [t.strip().lower() for t in (tags or []) if t.strip()],
        "content": content.strip()
    }

    data["entries"].append(entry)
    save_vault(data, vault_path)
    return entry

def search_entries(query, vault_path=DEFAULT_VAULT_PATH):
    """Searches entries by keyword across title, tags, and content."""
    data = load_vault(vault_path)
    q = query.lower()
    matches = []

    for item in data.get("entries", []):
        text = f"{item['title']} {' '.join(item.get('tags', []))} {item['content']}".lower()
        if q in text:
            matches.append(item)
    return matches

def export_decisions_md(out_path="DECISIONS.md", vault_path=DEFAULT_VAULT_PATH):
    """Compiles all recorded ADRs and lessons into canonical DECISIONS.md."""
    data = load_vault(vault_path)
    entries = data.get("entries", [])

    adrs = [e for e in entries if e["category"] == "adr"]
    quirks = [e for e in entries if e["category"] == "quirk"]
    lessons = [e for e in entries if e["category"] == "lesson"]

    md = [
        "# Architectural Decisions & Persistent Memory (ADRs)",
        "",
        "> Authoritative record of architectural decisions, tooling quirks, and operational lessons.",
        f"> Last updated: `{datetime.now().strftime('%Y-%m-%d %H:%M')}`",
        "",
        "---",
        "",
        "## 🏛️ Architecture Decision Records (ADRs)",
        ""
    ]

    if adrs:
        for a in adrs:
            tags_str = f" `[{', '.join(a['tags'])}]`" if a.get("tags") else ""
            md.extend([
                f"### {a['id']}: {a['title']}{tags_str}",
                f"*Recorded on {a['date']}*",
                "",
                a['content'],
                ""
            ])
    else:
        md.append("*No ADRs recorded yet.*\n")

    md.extend([
        "---",
        "",
        "## ⚡ Tooling & Platform Quirks",
        ""
    ])

    if quirks:
        for q in quirks:
            tags_str = f" `[{', '.join(q['tags'])}]`" if q.get("tags") else ""
            md.extend([
                f"### {q['id']}: {q['title']}{tags_str}",
                f"*Recorded on {q['date']}*",
                "",
                q['content'],
                ""
            ])
    else:
        md.append("*No quirks recorded yet.*\n")

    md.extend([
        "---",
        "",
        "## 💡 Post-Mortem Lessons Learned",
        ""
    ])

    if lessons:
        for l in lessons:
            tags_str = f" `[{', '.join(l['tags'])}]`" if l.get("tags") else ""
            md.extend([
                f"### {l['id']}: {l['title']}{tags_str}",
                f"*Recorded on {l['date']}*",
                "",
                l['content'],
                ""
            ])
    else:
        md.append("*No post-mortem lessons recorded yet.*\n")

    out_file = Path(out_path)
    out_file.write_text("\n".join(md), encoding="utf-8")
    return out_file

def print_summary(vault_path=DEFAULT_VAULT_PATH):
    """Outputs compact digest for /hub ingestion."""
    data = load_vault(vault_path)
    entries = data.get("entries", [])
    if not entries:
        print("[til-vault] Memory vault is empty.")
        return

    print(f"[til-vault] Indexed Knowledge Base ({len(entries)} entries):")
    for e in entries[-5:]:
        cat_badge = {"adr": "🏛️ ADR", "quirk": "⚡ QUIRK", "lesson": "💡 LESSON"}.get(e["category"], "ENTRY")
        print(f"  • [{cat_badge}] {e['id']}: {e['title']}")

def main():
    parser = argparse.ArgumentParser(description="Persistent Agent Memory & Decision Log / ADR Manager")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Record command
    p_record = subparsers.add_parser("record", help="Record a new memory or ADR")
    p_record.add_argument("--title", required=True, help="Title of entry")
    p_record.add_argument("--category", choices=["adr", "quirk", "lesson"], default="lesson", help="Category type")
    p_record.add_argument("--content", required=True, help="Detailed explanation / decision context")
    p_record.add_argument("--tags", nargs="*", help="Tags (e.g. windows powershell auth)")

    # Query command
    p_query = subparsers.add_parser("query", help="Search vault by keyword")
    p_query.add_argument("term", help="Search term")

    # List command
    p_list = subparsers.add_parser("list", help="List all entries in vault")

    # Export command
    p_export = subparsers.add_parser("export-adr", help="Export to canonical DECISIONS.md")
    p_export.add_argument("--out", default="DECISIONS.md", help="Output file path")

    # Summary command
    p_sum = subparsers.add_parser("summary", help="Compact summary for /hub")

    args = parser.parse_args()

    if args.command == "record":
        entry = record_entry(args.title, args.category, args.content, args.tags)
        print(f"[til-vault] Successfully saved {entry['category'].upper()} entry {entry['id']}: '{entry['title']}'")

    elif args.command == "query":
        results = search_entries(args.term)
        print(f"\n[til-vault] Search matches for '{args.term}' ({len(results)} found):")
        for r in results:
            print(f"\n  [{r['id']}] ({r['category'].upper()}) {r['title']} - {r['date']}")
            print(f"  Tags: {', '.join(r.get('tags', []))}")
            print(f"  Content:\n    {r['content']}")

    elif args.command == "list":
        data = load_vault()
        entries = data.get("entries", [])
        print(f"\n[til-vault] Total Indexed Memories: {len(entries)}")
        for r in entries:
            print(f"  • {r['id']:<8} | {r['category'].upper():<7} | {r['title']}")

    elif args.command == "export-adr":
        out = export_decisions_md(args.out)
        print(f"[til-vault] Compiled architectural records to: {out.resolve()}")

    elif args.command == "summary":
        print_summary()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
