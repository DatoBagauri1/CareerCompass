import os
import json
import logging
from typing import Optional
from flask import current_app

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    # If reportlab is not available, we'll create a simple HTML report instead
    REPORTLAB_AVAILABLE = False
    letter = None
    getSampleStyleSheet = None
    ParagraphStyle = None
    Paragraph = None
    Spacer = None
    TA_CENTER = None
    colors = None
    SimpleDocTemplate = None

def generate_pdf_report(analysis) -> Optional[str]:
    """Generate a PDF report for resume analysis."""
    try:
        report_filename = f"resume_report_{analysis.id}.pdf"
        report_path = os.path.join(current_app.config['REPORTS_FOLDER'], report_filename)
        
        if not REPORTLAB_AVAILABLE:
            # Generate HTML report instead
            return generate_html_report(analysis)
        
        # Create PDF document
        doc = SimpleDocTemplate(report_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        story.append(Paragraph("Resume Analysis Report", title_style))
        story.append(Spacer(1, 20))
        
        # ATS Score section
        ats_style = ParagraphStyle(
            'ATSScore',
            parent=styles['Heading2'],
            fontSize=18,
            spaceAfter=15,
            textColor=colors.darkgreen
        )
        story.append(Paragraph(f"ATS Score: {analysis.ats_score}%", ats_style))
        story.append(Spacer(1, 15))
        
        # Skills section
        story.append(Paragraph("Extracted Skills", styles['Heading2']))
        skills = json.loads(analysis.extracted_skills) if analysis.extracted_skills else {'technical': [], 'soft': []}
        
        if skills.get('technical'):
            story.append(Paragraph("<b>Technical Skills:</b>", styles['Normal']))
            tech_skills_text = ", ".join(skills['technical'])
            story.append(Paragraph(tech_skills_text, styles['Normal']))
            story.append(Spacer(1, 10))
        
        if skills.get('soft'):
            story.append(Paragraph("<b>Soft Skills:</b>", styles['Normal']))
            soft_skills_text = ", ".join(skills['soft'])
            story.append(Paragraph(soft_skills_text, styles['Normal']))
            story.append(Spacer(1, 15))
        
        # Missing keywords section
        missing_keywords = json.loads(analysis.missing_keywords) if analysis.missing_keywords else []
        if missing_keywords:
            story.append(Paragraph("Missing Keywords", styles['Heading2']))
            missing_text = ", ".join(missing_keywords[:10])  # Limit to first 10
            story.append(Paragraph(missing_text, styles['Normal']))
            story.append(Spacer(1, 15))
        
        # Suggestions section
        suggestions = json.loads(analysis.suggestions) if analysis.suggestions else []
        if suggestions:
            story.append(Paragraph("LinkedIn Headline Suggestions", styles['Heading2']))
            for i, suggestion in enumerate(suggestions, 1):
                story.append(Paragraph(f"{i}. {suggestion}", styles['Normal']))
            story.append(Spacer(1, 15))
        
        # Job description section (if provided)
        if analysis.job_description:
            story.append(Paragraph("Job Description Used", styles['Heading2']))
            job_desc_text = analysis.job_description[:500] + "..." if len(analysis.job_description) > 500 else analysis.job_description
            story.append(Paragraph(job_desc_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        return report_path
        
    except Exception as e:
        logging.error(f"Error generating PDF report: {str(e)}")
        # Fallback to HTML report
        return generate_html_report(analysis)

def generate_html_report(analysis) -> Optional[str]:
    """Generate an HTML report as fallback when PDF generation fails."""
    try:
        report_filename = f"resume_report_{analysis.id}.html"
        report_path = os.path.join(current_app.config['REPORTS_FOLDER'], report_filename)
        
        skills = json.loads(analysis.extracted_skills) if analysis.extracted_skills else {'technical': [], 'soft': []}
        missing_keywords = json.loads(analysis.missing_keywords) if analysis.missing_keywords else []
        suggestions = json.loads(analysis.suggestions) if analysis.suggestions else []
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Resume Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                .header {{ text-align: center; color: #1e40af; margin-bottom: 30px; }}
                .score {{ font-size: 24px; color: #059669; font-weight: bold; margin: 20px 0; }}
                .section {{ margin: 20px 0; }}
                .section h2 {{ color: #374151; border-bottom: 2px solid #e5e7eb; padding-bottom: 5px; }}
                .skills {{ background: #f3f4f6; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                .suggestion {{ background: #eff6ff; padding: 10px; margin: 5px 0; border-left: 4px solid #3b82f6; }}
                .keywords {{ color: #dc2626; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Resume Analysis Report</h1>
                <div class="score">ATS Score: {analysis.ats_score}%</div>
            </div>
            
            <div class="section">
                <h2>Extracted Skills</h2>
                {f'<div class="skills"><strong>Technical Skills:</strong> {", ".join(skills.get("technical", []))}</div>' if skills.get("technical") else ''}
                {f'<div class="skills"><strong>Soft Skills:</strong> {", ".join(skills.get("soft", []))}</div>' if skills.get("soft") else ''}
            </div>
            
            {f'''<div class="section">
                <h2>Missing Keywords</h2>
                <div class="keywords">{", ".join(missing_keywords[:15])}</div>
            </div>''' if missing_keywords else ''}
            
            {f'''<div class="section">
                <h2>LinkedIn Headline Suggestions</h2>
                {"".join([f'<div class="suggestion">{i}. {suggestion}</div>' for i, suggestion in enumerate(suggestions, 1)])}
            </div>''' if suggestions else ''}
            
            {f'''<div class="section">
                <h2>Job Description Used</h2>
                <p>{analysis.job_description[:500] + "..." if len(analysis.job_description) > 500 else analysis.job_description}</p>
            </div>''' if analysis.job_description else ''}
            
            <div class="section">
                <small>Report generated on {analysis.analysis_time.strftime('%Y-%m-%d %H:%M:%S')}</small>
            </div>
        </body>
        </html>
        """
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return report_path
        
    except Exception as e:
        logging.error(f"Error generating HTML report: {str(e)}")
        return None
