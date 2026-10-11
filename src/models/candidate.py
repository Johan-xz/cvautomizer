from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Experience(BaseModel):
    title: str
    company: str
    start: date
    end: Optional[date] = None
    description: str

class Skill(BaseModel):
    name: str
    level: str

class Education(BaseModel):
    degree: str
    school: str
    year: int

class Candidate(BaseModel):
    name: str
    email: str
    experience: List[Experience]
    skills: List[Skill]
    education: List[Education]
