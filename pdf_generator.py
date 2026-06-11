# pdf_generator.py

import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

def get_safe_filepath(data):
    """Handles absolute path routing and defensive system writing."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "resumes")
    
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        safe_name = "".join(x for x in data.get('name', 'resume') if x.isalnum()).lower()
        filepath = os.path.join(output_dir, f"{safe_name}_resume.pdf")
        with open(filepath, "a"): pass
    except (OSError, PermissionError):
        output_dir = str(Path.home() / "Downloads")
        safe_name = "".join(x for x in data.get('name', 'resume') if x.isalnum()).lower()
        filepath = os.path.join(output_dir, f"{safe_name}_resume.pdf")
        
    return filepath


def compile_minimalist_pdf(data, filepath):
    """Template: Elite Minimalist Layout featuring horizontal rules under headings."""
    doc = SimpleDocTemplate(filepath, pagesize=letter, leftMargin=40, rightMargin=40, topMargin=35, bottomMargin=35)
    story = []
    styles = getSampleStyleSheet()
    
    name_style = ParagraphStyle('MinName', parent=styles['Heading1'], fontSize=20, leading=24, alignment=TA_CENTER, textColor='#000000')
    contact_style = ParagraphStyle('MinContact', parent=styles['Normal'], fontSize=9, leading=13, alignment=TA_CENTER, textColor='#333333')
    heading_style = ParagraphStyle('MinHead', parent=styles['Heading2'], fontSize=11, leading=14, spaceBefore=8, spaceAfter=2, textColor='#000000')
    body_style = ParagraphStyle('MinBody', parent=styles['Normal'], fontSize=9.5, leading=13.5, spaceAfter=4, textColor='#111111')
    
    def add_section_header(title_text):
        story.append(Paragraph(f"<b>{title_text}</b>", heading_style))
        story.append(HRFlowable(width="100%", thickness=0.75, color='#222222', spaceBefore=1, spaceAfter=6))

    # Name & Contact Header Block
    story.append(Paragraph(f"<b>{data.get('name', 'YOUR NAME')}</b>", name_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph(data.get('contact', ''), contact_style))
    story.append(Spacer(1, 10))
    
    # 1. Summary
    add_section_header("Summary")
    story.append(Paragraph(data.get('summary', ''), body_style))
    
    # 2. Skills
    add_section_header("Skills")
    skills_csv = ", ".join(data.get('skills', []))
    story.append(Paragraph(skills_csv, body_style))
    
    # 3. Experience
    if data.get('experience'):
        add_section_header("Experience")
        for item in data.get('experience', []):
            story.append(Paragraph(f"• {item}", body_style))
        
    # 4. Projects
    if data.get('projects'):
        add_section_header("Projects")
        for item in data.get('projects', []):
            story.append(Paragraph(f"• {item}", body_style))
        
    # 5. Education
    add_section_header("Education")
    for item in data.get('education', []):
        story.append(Paragraph(f"• {item}", body_style))
        
    # 6. Certificates
    if data.get('certificates'):
        add_section_header("Certificates")
        for item in data.get('certificates', []):
            story.append(Paragraph(f"• {item}", body_style))
        
    doc.build(story)


def compile_pdf(data, theme_color="#1A365D", template_style="Elite Minimalist"):
    """Main routing function switcher."""
    filepath = get_safe_filepath(data)
    compile_minimalist_pdf(data, filepath)
    return filepath