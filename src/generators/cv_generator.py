from src.models.candidate import Candidate
from src.models.job_offer import JobOffer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import json
from datetime import datetime

class CVGenerator:
    """
    Harvard Format CV Generator
    Dinámico, minimalista, ATS-compatible
    """
    
    def __init__(self, candidate: Candidate, job_offer: JobOffer, match_result: dict):
        self.candidate = candidate
        self.job_offer = job_offer
        self.match_result = match_result
        self.matched_skills = match_result.get('matched_skills', [])
    
    def generate_pdf(self, filepath: str):
        """Genera PDF en formato Harvard"""
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch,
            leftMargin=1*inch,
            rightMargin=1*inch
        )
        
        story = []
        styles = self._create_harvard_styles()
        
        # === HEADER ===
        story.extend(self._build_header(styles))
        
        # === PROFESSIONAL SUMMARY ===
        if self.candidate.about_me:
            story.extend(self._build_summary(styles))
        
        # === EXPERIENCE ===
        story.extend(self._build_experience(styles))
        
        # === EDUCATION ===
        story.extend(self._build_education(styles))
        
        # === LEADERSHIP & ACTIVITIES ===
        if self.candidate.leadership:
            story.extend(self._build_leadership(styles))
        
        # === SKILLS ===
        story.extend(self._build_skills(styles))
        
        # === LANGUAGES ===
        if self.candidate.skills.get('languages'):
            story.extend(self._build_languages(styles))
        
        # === INTERESTS ===
        if self.candidate.interests:
            story.extend(self._build_interests(styles))
        
        doc.build(story)
    
    def _create_harvard_styles(self):
        """Harvard format styles - minimalista y limpio"""
        styles = getSampleStyleSheet()
        
        # Nombre (Harvard: grande, bold, centrado)
        styles.add(ParagraphStyle(
            name='HarvardName',
            parent=styles['Normal'],
            fontSize=16,
            textColor=colors.black,
            spaceAfter=4,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Contacto (una línea, centrado)
        styles.add(ParagraphStyle(
            name='HarvardContact',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.black,
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Section Headers (Harvard: bold, sin decoraciones)
        styles.add(ParagraphStyle(
            name='HarvardSection',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=4,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        ))
        
        # Job Title / Position (bold)
        styles.add(ParagraphStyle(
            name='HarvardJobTitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=1,
            fontName='Helvetica-Bold'
        ))
        
        # Company + Dates (normal, en línea)
        styles.add(ParagraphStyle(
            name='HarvardCompanyDates',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=2,
            fontName='Helvetica'
        ))
        
        # Bullet Description
        styles.add(ParagraphStyle(
            name='HarvardBullet',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=2,
            leftIndent=0.2*inch,
            fontName='Helvetica'
        ))
        
        # Body text (para resúmenes, descripciones)
        styles.add(ParagraphStyle(
            name='HarvardBody',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=4,
            fontName='Helvetica'
        ))
        
        # Skills inline
        styles.add(ParagraphStyle(
            name='HarvardSkills',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=2,
            fontName='Helvetica'
        ))
        
        return styles
    
    def _build_header(self, styles):
        """
        HEADER - Harvard style
        Nombre
        Email • Phone • Location
        """
        content = []
        
        # Nombre
        content.append(Paragraph(self.candidate.name, styles['HarvardName']))
        
        # Contacto en una línea
        contact_parts = []
        if self.candidate.email:
            contact_parts.append(self.candidate.email)
        if self.candidate.phone:
            contact_parts.append(self.candidate.phone)
        if self.candidate.location:
            contact_parts.append(self.candidate.location)
        
        contact_str = " • ".join(contact_parts)
        content.append(Paragraph(contact_str, styles['HarvardContact']))
        content.append(Spacer(1, 0.1*inch))
        
        return content
    
    def _build_summary(self, styles):
        """PROFESSIONAL SUMMARY"""
        content = []
        content.append(Paragraph("PROFESSIONAL SUMMARY", styles['HarvardSection']))
        content.append(Paragraph(self.candidate.about_me.strip(), styles['HarvardBody']))
        content.append(Spacer(1, 0.05*inch))
        return content
    
    def _build_experience(self, styles):
        """EXPERIENCE - Harvard format"""
        content = []
        content.append(Paragraph("EXPERIENCE", styles['HarvardSection']))
        
        for exp in self.candidate.experience:
            if not exp.show:
                continue
            
            # Título | Empresa
            header = f"{exp.title} | {exp.company}"
            content.append(Paragraph(header, styles['HarvardJobTitle']))
            
            # Fechas | Ubicación
            dates = f"{exp.start_date} – {exp.end_date if exp.end_date else 'Present'}"
            company_line = f"{dates} | {exp.location}"
            content.append(Paragraph(company_line, styles['HarvardCompanyDates']))
            
            # Bullets
            for bullet in exp.bullets:
                bullet_text = self._highlight_matched_skills(bullet)
                content.append(Paragraph(f"• {bullet_text}", styles['HarvardBullet']))
            
            content.append(Spacer(1, 0.05*inch))
        
        return content
    
    def _build_education(self, styles):
        """EDUCATION - Harvard format"""
        content = []
        content.append(Paragraph("EDUCATION", styles['HarvardSection']))
        
        for edu in self.candidate.education:
            if not edu.show:
                continue
            
            # Degree
            content.append(Paragraph(edu.degree, styles['HarvardJobTitle']))
            
            # School, Year, Location
            school_line = f"{edu.school} | {edu.year}"
            if edu.location:
                school_line += f" | {edu.location}"
            
            content.append(Paragraph(school_line, styles['HarvardCompanyDates']))
            content.append(Spacer(1, 0.05*inch))
        
        return content
    
    def _build_leadership(self, styles):
        """LEADERSHIP & ACTIVITIES - Harvard format"""
        content = []
        content.append(Paragraph("LEADERSHIP & ACTIVITIES", styles['HarvardSection']))
        
        for activity in self.candidate.leadership:
            if not activity.show:
                continue
            
            # Title | Organization
            header = f"{activity.title} | {activity.organization}"
            content.append(Paragraph(header, styles['HarvardJobTitle']))
            
            # Date | Location
            date_line = f"{activity.date}"
            if activity.location:
                date_line += f" | {activity.location}"
            
            content.append(Paragraph(date_line, styles['HarvardCompanyDates']))
            
            # Description
            content.append(Paragraph(activity.description.strip(), styles['HarvardBody']))
            content.append(Spacer(1, 0.05*inch))
        
        return content
    
    def _build_skills(self, styles):
        """SKILLS - Harvard format (inline, separado por comas)"""
        content = []
        content.append(Paragraph("SKILLS", styles['HarvardSection']))
        
        # Technical Skills
        if self.candidate.skills.get('technical'):
            tech = ", ".join(self.candidate.skills['technical'])
            tech = self._highlight_matched_skills(tech)
            content.append(Paragraph(f"<b>Technical:</b> {tech}", styles['HarvardSkills']))
        
        # Laboratory Skills
        if self.candidate.skills.get('laboratory'):
            lab = ", ".join(self.candidate.skills['laboratory'])
            lab = self._highlight_matched_skills(lab)
            content.append(Paragraph(f"<b>Laboratory:</b> {lab}", styles['HarvardSkills']))
        
        content.append(Spacer(1, 0.05*inch))
        return content
    
    def _build_languages(self, styles):
        """LANGUAGES - Harvard format"""
        content = []
        content.append(Paragraph("LANGUAGES", styles['HarvardSection']))
        
        langs = []
        for lang in self.candidate.skills['languages']:
            langs.append(f"{lang['name']} ({lang['level'].capitalize()})")
        
        langs_str = ", ".join(langs)
        content.append(Paragraph(langs_str, styles['HarvardSkills']))
        content.append(Spacer(1, 0.05*inch))
        
        return content
    
    def _build_interests(self, styles):
        """INTERESTS - Harvard format"""
        content = []
        content.append(Paragraph("INTERESTS", styles['HarvardSection']))
        
        interests_str = ", ".join(self.candidate.interests)
        content.append(Paragraph(interests_str, styles['HarvardSkills']))
        
        return content
    
    def _highlight_matched_skills(self, text):
        """
        Destaca skills que matchean con la oferta
        (Placeholder para futura mejora con bold/color)
        """
        return text
    
    def generate_analysis(self, filepath: str):
        """Genera JSON con análisis detallado de match"""
        analysis = {
            'generated_at': datetime.now().isoformat(),
            'candidate': {
                'name': self.candidate.name,
                'email': self.candidate.email,
                'location': self.candidate.location
            },
            'job_offer': {
                'title': self.job_offer.title,
                'company': self.job_offer.company
            },
            'match_results': {
                'overall_match_percentage': self.match_result['match_percentage'],
                'matched_skills': self.match_result['matched_skills'],
                'missing_skills': self.match_result['missing_skills'],
                'total_required_skills': len(self.job_offer.required_skills),
                'total_matched_skills': len(self.match_result['matched_skills'])
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)