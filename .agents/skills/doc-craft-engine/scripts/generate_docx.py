#!/usr/bin/env python3
"""
generate_docx.py - Generates publication-grade styled DOCX files using DOC_STYLE.json
"""

import sys
import os
import json
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return RGBColor(*(int(hex_str[i:i+2], 16) for i in (0, 2, 4)))

def set_cell_background(cell, hex_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color.lstrip("#")}"/>')
    tcPr.append(shd)

def create_styled_docx(content_md_path, style_json_path, output_docx_path):
    # Load style
    style = {
        "typography": {"primaryFont": "Arial", "defaultBodyPt": 11, "h1Pt": 18, "h2Pt": 14},
        "palette": {"accentPrimary": "#0284c7", "surfaceSecondary": "#f8fafc", "border": "#e2e8f0"},
        "geometry": {"topMarginInches": 1.0, "bottomMarginInches": 1.0, "leftMarginInches": 1.0, "rightMarginInches": 1.0}
    }
    if os.path.exists(style_json_path):
        with open(style_json_path, 'r', encoding='utf-8') as f:
            style.update(json.load(f))

    doc = docx.Document()
    
    # Configure margins
    section = doc.sections[0]
    geom = style.get("geometry", {})
    section.top_margin = Inches(geom.get("topMarginInches", 1.0))
    section.bottom_margin = Inches(geom.get("bottomMarginInches", 1.0))
    section.left_margin = Inches(geom.get("leftMarginInches", 1.0))
    section.right_margin = Inches(geom.get("rightMarginInches", 1.0))
    
    accent_rgb = hex_to_rgb(style.get("palette", {}).get("accentPrimary", "#0284c7"))
    font_name = style.get("typography", {}).get("primaryFont", "Calibri")
    
    # Configure Normal style font
    normal_style = doc.styles['Normal']
    normal_style.font.name = font_name
    normal_style.font.size = Pt(style.get("typography", {}).get("defaultBodyPt", 11))
    normal_style.font.color.rgb = RGBColor(51, 65, 85) # Slate-700
    
    with open(content_md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
            
        if line_clean.startswith("# "):
            title_text = line_clean[2:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            run = p.add_run(title_text)
            run.font.name = font_name
            run.font.size = Pt(style.get("typography", {}).get("h1Pt", 20))
            run.font.bold = True
            run.font.color.rgb = accent_rgb
            
        elif line_clean.startswith("## "):
            h2_text = line_clean[3:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(h2_text)
            run.font.name = font_name
            run.font.size = Pt(style.get("typography", {}).get("h2Pt", 15))
            run.font.bold = True
            run.font.color.rgb = RGBColor(30, 41, 59)
            
        elif line_clean.startswith("### "):
            h3_text = line_clean[4:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(h3_text)
            run.font.name = font_name
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(71, 85, 105)
            
        elif line_clean.startswith("> "):
            # Callout Box
            callout_text = line_clean[2:].strip()
            table = doc.add_table(rows=1, cols=1)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            cell = table.cell(0, 0)
            set_cell_background(cell, style.get("palette", {}).get("surfaceSecondary", "#f8fafc"))
            
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run("💡 " + callout_text)
            run.font.name = font_name
            run.font.size = Pt(10)
            run.font.italic = True
            run.font.color.rgb = accent_rgb
            
        elif line_clean.startswith("- ") or line_clean.startswith("* "):
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(3)
            bullet_text = line_clean[2:].strip()
            run = p.add_run(bullet_text)
            run.font.name = font_name
            
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.25
            run = p.add_run(line_clean)
            run.font.name = font_name

    os.makedirs(os.path.dirname(os.path.abspath(output_docx_path)), exist_ok=True)
    doc.save(output_docx_path)
    print(f"Successfully generated styled DOCX: {output_docx_path}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_docx.py <content_markdown_path> <style_json_path> [output_docx_path]")
        sys.exit(1)
        
    content_path = sys.argv[1]
    style_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else "output/document.docx"
    
    create_styled_docx(content_path, style_path, output_path)

if __name__ == "__main__":
    main()
