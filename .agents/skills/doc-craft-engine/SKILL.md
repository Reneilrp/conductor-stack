---
name: doc-craft-engine
description: Audits reference documents (.docx, .pptx, .pdf) to extract typography, margins, and 60-30-10 palettes, then generates publication-grade styled Word, PowerPoint, and PDF deliverables using bundled Python automation scripts. Use with /doc-craft, /audit-doc, or /generate-doc.
---

# Document Craft Engine

Use this skill whenever you need to **extract visual formatting from an existing reference document** or **generate branded, publication-ready DOCX, PPTX, or PDF deliverables** for a project.

It eliminates generic, unstyled documents by pairing **Reference Document Auditing** with **Python-Powered Typesetting** (`python-docx`, `python-pptx`, `pymupdf`).

---

## The 2 Core Operating Modes

```
                              [User Request]
                                    │
            ┌───────────────────────┴───────────────────────┐
            ▼                                               ▼
[Mode 1: Reference Audit (/audit-doc)]        [Mode 2: Generate Doc (/generate-doc)]
  • Parses sample .docx, .pptx, or .pdf         • Reads project's DOC_STYLE.json
  • Extracts fonts, sizes, margins, colors      • Ingests markdown or slide data
  • Generates docs/DOC_STYLE.json & .md         • Compiles styled DOCX or PPTX
```

---

## Mode 1: Style Audit & Reference Extraction

When the user provides a reference file (e.g. `templates/company_report.docx` or `deck.pptx`):

### 1. Run the Audit Script
* **On Windows:**
  ```powershell
  py -3 .agents/skills/doc-craft-engine/scripts/audit_doc.py <path_to_reference> docs/
  ```
* **On Linux / WSL:**
  ```bash
  python3 ~/.agents/skills/doc-craft-engine/scripts/audit_doc.py <path_to_reference> docs/
  ```

### 2. Output Generated
The script outputs:
1. `docs/DOC_STYLE.json`: Machine-readable token dictionary with exact font families, font sizes (title, H1, H2, body), margins, and 60-30-10 color hexes.
2. `docs/DOC_STYLE.md`: A readable visual specification summary.

---

## Mode 2: Publication-Grade Document Generation

When the user asks to generate a document or presentation:

### 1. Generating Word Documents (`.docx`)
1. Create or read the content markdown file (e.g. `docs/architecture-overview.md`).
2. Run the compiler:
   * **On Windows:**
     ```powershell
     py -3 .agents/skills/doc-craft-engine/scripts/generate_docx.py docs/content.md docs/DOC_STYLE.json output/Final_Report.docx
     ```
   * **On Linux / WSL:**
     ```bash
     python3 ~/.agents/skills/doc-craft-engine/scripts/generate_docx.py docs/content.md docs/DOC_STYLE.json output/Final_Report.docx
     ```
3. **Features Built In:**
   * Margins matched exactly from the style profile.
   * Heading 1/2/3 styled with proper hierarchy and accent colors.
   * Styled callout alert boxes with background fills and accent colored text.
   * Proper line spacing (1.25) and paragraph margins.

---

### 2. Generating Presentation Slide Decks (`.pptx`)
1. Draft the slide deck structure in JSON format (e.g. `docs/deck.json` with titles, subtitles, and card points).
2. Run the compiler:
   * **On Windows:**
     ```powershell
     py -3 .agents/skills/doc-craft-engine/scripts/generate_pptx.py docs/deck.json docs/DOC_STYLE.json output/Presentation.pptx
     ```
   * **On Linux / WSL:**
     ```bash
     python3 ~/.agents/skills/doc-craft-engine/scripts/generate_pptx.py docs/deck.json docs/DOC_STYLE.json output/Presentation.pptx
     ```
3. **Features Built In:**
   * 16:9 modern widescreen format.
   * Multi-column card containers with rounded borders.
   * High-contrast accent color applied to titles and key indicators.

---

## Summary of Commands

| Command | Purpose |
|---|---|
| `/audit-doc <file>` | Inspects a sample document and generates `DOC_STYLE.json` + `DOC_STYLE.md`. |
| `/generate-doc <md>` | Uses `DOC_STYLE.json` to compile a styled `.docx`. |
| `/generate-deck <json>` | Uses `DOC_STYLE.json` to compile a 16:9 `.pptx`. |
| `/doc-craft` | General workflow router for document styling and publishing. |
