from src.models.candidate import Candidate
from src.models.job_offer import JobOffer

class CVMatcher:
    def __init__(self, candidate: Candidate, job_offer: JobOffer):
        self.candidate = candidate
        self.job_offer = job_offer
    
    def calculate_match(self) -> dict:
        """Calcula match entre candidato y oferta"""
        candidate_skills = [s.name.lower() for s in self.candidate.skills]
        required_skills = [s.lower() for s in self.job_offer.required_skills]
        
        matched_skills = [s for s in required_skills if s in candidate_skills]
        match_percentage = (len(matched_skills) / len(required_skills)) * 100
        
        return {
            'match_percentage': round(match_percentage, 2),
            'matched_skills': matched_skills,
            'missing_skills': [s for s in required_skills if s not in candidate_skills]
        }
