import json
from pathlib import Path
from src.models.job_offer import JobOffer

class JobOfferAnalyzer:
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
    
    def analyze(self) -> JobOffer:
        """Parsea y extrae info de la oferta"""
        if self.filepath.suffix == '.json':
            return self._parse_json()
        else:
            raise ValueError("Solo JSON por ahora")
    
    def _parse_json(self) -> JobOffer:
        with open(self.filepath) as f:
            data = json.load(f)
        return JobOffer(**data)