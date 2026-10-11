from pydantic import BaseModel
from typing import List

class JobOffer(BaseModel):
    title: str
    company: str
    description: str
    required_skills: List[str]
    experience_years: int
    keywords: List[str]