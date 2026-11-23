#!/usr/bin/env python3
"""
audit_doc.py - Audits reference documents (.docx, .pptx, .pdf) to extract visual styling DNA.
Generates DOC_STYLE.json and DOC_STYLE.md.
"""

import sys
import os
import json
from pathlib import Path

def audit_docx(file_path):
    import docx
    from docx.shared import Inches, Pt, RGBColor
    
    doc = docx.Document(file_path)
    style_info = {
        "format": "docx",
        "file": os.path.basename(file_path),
        "typography": {},
        "geometry": {},
        "palette": {
            "baseCanvas": "#ffffff",
            "surfaceSecondary": "#f8fafc",
            "accentPrimary": "#0284c7"
        }
    }
    
    # Extract margins from the first section
    if doc.sections:
        s = doc.sections[0]
        style_info["geometry"] = {
            "pageWidthInches": round(s.page_width.inches, 2) if s.page_width else 8.5,
            "pageHeightInches": round(s.page_height.inches, 2) if s.page_height else 11.0,
            "topMarginInches": round(s.top_margin.inches, 2) if s.top_margin else 1.0,
            "bottomMarginInches": round(s.bottom_margin.inches, 2) if s.bottom_margin else 1.0,
            "leftMarginInches": round(s.left_margin.inches, 2) if s.left_margin else 1.0,
            "rightMarginInches": round(s.right_margin.inches, 2) if s.right_margin else 1.0,
        }
    
    # Inspect styles and fonts
    font_names = set()
    for s in doc.styles:
        if hasattr(s, 'font') and s.font and s.font.name:
            font_names.add(s.font.name)
            
    # Sample paragraphs to detect actual fonts and sizes
    for p in doc.paragraphs[:20]:
        for r in p.runs:
            if r.font and r.font.name:
                font_names.add(r.font.name)
            if r.font and r.font.color and r.font.color.rgb:
                hex_col = f"#{r.font.color.rgb}"
                if hex_col.lower() not in ["#000000", "#ffffff"]:
                    style_info["palette"]["accentPrimary"] = hex_col
                    
    font_list = list(font_names)
    style_info["typography"] = {
        "primaryFont": font_list[0] if font_list else "Calibri",
        "detectedFonts": font_list,
        "defaultBodyPt": 11.0,
        "h1Pt": 18.0,
        "h2Pt": 14.0
    }
    return style_info

def audit_pptx(file_path):
    from pptx import Presentation
    from pptx.util import Inches, Pt
    
    prs = Presentation(file_path)
    style_info = {
        "format": "pptx",
        "file": os.path.basename(file_path),
        "geometry": {
            "slideWidthInches": round(prs.slide_width.inches, 2),
            "slideHeightInches": round(prs.slide_height.inches, 2),
            "isWidescreen": round(prs.slide_width.inches / prs.slide_height.inches, 2) == 1.78
        },
        "typography": {
            "titleFont": "Arial",
            "bodyFont": "Calibri",
            "detectedFonts": []
        },
        "palette": {
            "baseCanvas": "#ffffff",
            "surfaceSecondary": "#f1f5f9",
            "accentPrimary": "#0284c7"
        }
    }
    
    fonts = set()
    for slide in prs.slides[:5]:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        if run.font.name:
                            fonts.add(run.font.name)
                        if run.font.color and hasattr(run.font.color, 'rgb') and run.font.color.rgb:
                            hex_c = f"#{run.font.color.rgb}"
                            if hex_c.lower() not in ["#000000", "#ffffff"]:
                                style_info["palette"]["accentPrimary"] = hex_c
                                
    font_list = list(fonts)
    if font_list:
        style_info["typography"]["titleFont"] = font_list[0]
        style_info["typography"]["bodyFont"] = font_list[1] if len(font_list) > 1 else font_list[0]
        style_info["typography"]["detectedFonts"] = font_list
        
    return style_info

def audit_pdf(file_path):
    import fitz  # PyMuPDF
    
    doc = fitz.open(file_path)
    style_info = {
        "format": "pdf",
        "file": os.path.basename(file_path),
        "pageCount": len(doc),
        "typography": {"detectedFonts": []},
        "geometry": {},
        "palette": {
            "baseCanvas": "#ffffff",
            "surfaceSecondary": "#f8fafc",
            "accentPrimary": "#0284c7"
        }
    }
    
    if len(doc) > 0:
        p = doc[0]
        rect = p.rect
        style_info["geometry"] = {
            "widthPt": round(rect.width, 2),
            "heightPt": round(rect.height, 2),
            "isA4": abs(rect.width - 595.3) < 5 and abs(rect.height - 841.9) < 5,
            "isLetter": abs(rect.width - 612.0) < 5 and abs(rect.height - 792.0) < 5
        }
        
        fonts = set()
        for font in p.get_fonts():
            fonts.add(font[3])  # font name
        style_info["typography"]["detectedFonts"] = list(fonts)
        style_info["typography"]["primaryFont"] = list(fonts)[0] if fonts else "Helvetica"
        
    return style_info

def main():
    if len(sys.argv) < 2:
        print("Usage: python audit_doc.py <path_to_reference_file> [output_dir]")
        sys.exit(1)
        
    target_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "docs"
    
    if not os.path.exists(target_file):
        print(f"Error: Target file '{target_file}' not found.")
        sys.exit(1)
        
    ext = Path(target_file).suffix.lower()
    if ext == ".docx":
        data = audit_docx(target_file)
    elif ext == ".pptx":
        data = audit_pptx(target_file)
    elif ext == ".pdf":
        data = audit_pdf(target_file)
    else:
        print(f"Unsupported file format: {ext}. Supported: .docx, .pptx, .pdf")
        sys.exit(1)
        
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, "DOC_STYLE.json")
    md_path = os.path.join(output_dir, "DOC_STYLE.md")
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Document Style Specification\n\n")
        f.write(f"Extracted from reference file: `{os.path.basename(target_file)}`\n\n")
        f.write(f"## 1. Typography\n")
        f.write(f"- **Primary Font:** {data['typography'].get('primaryFont', data['typography'].get('titleFont', 'Standard'))}\n")
        f.write(f"- **Detected Fonts:** {', '.join(data['typography'].get('detectedFonts', []))}\n\n")
        f.write(f"## 2. Geometry & Layout\n")
        for k, v in data["geometry"].items():
            f.write(f"- **{k}:** {v}\n")
        f.write(f"\n## 3. Color Palette (60-30-10)\n")
        for k, v in data["palette"].items():
            f.write(f"- **{k}:** `{v}`\n")
            
    print(f"Successfully generated style profile:")
    print(f" - JSON: {json_path}")
    print(f" - Markdown: {md_path}")

if __name__ == "__main__":
    main()
