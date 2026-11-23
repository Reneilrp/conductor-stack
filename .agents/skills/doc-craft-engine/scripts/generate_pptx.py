#!/usr/bin/env python3
"""
generate_pptx.py - Generates modern 16:9 presentation slide decks using DOC_STYLE.json
"""

import sys
import os
import json
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return RGBColor(*(int(hex_str[i:i+2], 16) for i in (0, 2, 4)))

def create_styled_pptx(slides_json_path, style_json_path, output_pptx_path):
    # Load style
    style = {
        "typography": {"titleFont": "Arial", "bodyFont": "Calibri"},
        "palette": {"accentPrimary": "#0284c7", "surfaceSecondary": "#f8fafc", "baseCanvas": "#ffffff"}
    }
    if os.path.exists(style_json_path):
        with open(style_json_path, 'r', encoding='utf-8') as f:
            style.update(json.load(f))
            
    # Load slides data
    with open(slides_json_path, 'r', encoding='utf-8') as f:
        deck_data = json.load(f)
        
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    accent_rgb = hex_to_rgb(style.get("palette", {}).get("accentPrimary", "#0284c7"))
    surface_rgb = hex_to_rgb(style.get("palette", {}).get("surfaceSecondary", "#f8fafc"))
    title_font = style.get("typography", {}).get("titleFont", "Arial")
    body_font = style.get("typography", {}).get("bodyFont", "Calibri")
    
    for slide_data in deck_data.get("slides", []):
        slide = prs.slides.add_slide(blank_layout)
        
        # Add Title
        title_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.333), Inches(1.2))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = slide_data.get("title", "Slide Title")
        p.font.name = title_font
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = accent_rgb
        
        # Add Subtitle / Category
        if "subtitle" in slide_data:
            p2 = tf.add_paragraph()
            p2.text = slide_data["subtitle"]
            p2.font.name = body_font
            p2.font.size = Pt(14)
            p2.font.color.rgb = RGBColor(100, 116, 139) # Slate-500
            
        # Add Cards / Points
        cards = slide_data.get("cards", [])
        if cards:
            num_cards = len(cards)
            card_width = (11.333 - (0.4 * (num_cards - 1))) / num_cards
            start_y = Inches(2.3)
            card_height = Inches(4.3)
            
            for i, card in enumerate(cards):
                card_x = Inches(1.0 + i * (card_width + 0.4))
                # Add background shape
                shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, card_x, start_y, Inches(card_width), card_height)
                shape.fill.solid()
                shape.fill.fore_color.rgb = surface_rgb
                shape.line.color.rgb = RGBColor(226, 232, 240)
                shape.line.width = Pt(1)
                
                # Add content inside card
                ctf = shape.text_frame
                ctf.word_wrap = True
                ctf.margin_left = Inches(0.3)
                ctf.margin_right = Inches(0.3)
                ctf.margin_top = Inches(0.4)
                
                cp1 = ctf.paragraphs[0]
                cp1.text = card.get("heading", "")
                cp1.font.name = title_font
                cp1.font.size = Pt(18)
                cp1.font.bold = True
                cp1.font.color.rgb = RGBColor(30, 41, 59)
                
                for pt in card.get("points", []):
                    cp = ctf.add_paragraph()
                    cp.text = "• " + pt
                    cp.font.name = body_font
                    cp.font.size = Pt(13)
                    cp.font.color.rgb = RGBColor(71, 85, 105)
                    cp.space_before = Pt(8)
                    
    os.makedirs(os.path.dirname(os.path.abspath(output_pptx_path)), exist_ok=True)
    prs.save(output_pptx_path)
    print(f"Successfully generated styled PPTX: {output_pptx_path}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_pptx.py <slides_json_path> <style_json_path> [output_pptx_path]")
        sys.exit(1)
        
    slides_path = sys.argv[1]
    style_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else "output/presentation.pptx"
    
    create_styled_pptx(slides_path, style_path, output_path)

if __name__ == "__main__":
    main()
