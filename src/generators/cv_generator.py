from src.models.candidate import Candidate
from src.models.job_offer import JobOffer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib import colors
import json

class CVGenerator:
    def __init__(self, candidate: Candidate, job_offer: JobOffer, match_result: dict):
        self.candidate = candidate
        self.job_offer = job_offer
        self.match_result = match_result
    
    def generate_pdf(self, filepath: str):
        doc = SimpleDocTemplate(filepath, pagesize=letter, topMargin=0.5*inch)
        story = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, alignment=1)
        heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=11)
        
        story.append(Paragraph(self.candidate.name, title_style))
        story.append(Paragraph(self.candidate.email, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        story.append(Paragraph("EXPERIENCE", heading_style))
        for exp in self.candidate.experience:
            story.append(Paragraph(f"<b>{exp.title}</b>, {exp.company}", styles['Normal']))
        
        story.append(Spacer(1, 0.15*inch))
        story.append(Paragraph("SKILLS", heading_style))
        matched = ', '.join(self.match_result['matched_skills'])
        story.append(Paragraph(matched, styles['Normal']))
        
        doc.build(story)
    
    def generate_analysis(self, filepath: str):
        analysis = {
            'candidate': self.candidate.name,
            'job': self.job_offer.title,
            'match': self.match_result['match_percentage'],
            'matched_skills': self.match_result['matched_skills'],
            'missing_skills': self.match_result['missing_skills']
        }
        with open(filepath, 'w') as f:
            json.dump(analysis, f, indent=2)
