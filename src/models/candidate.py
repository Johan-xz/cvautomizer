from pydantic import BaseModel
from typing import List, Optional


class Education(BaseModel):
    degree: str
    school: str
    location: Optional[str] = None
    year: int
    gpa: Optional[float] = None
    show: bool = True


class Experience(BaseModel):
    title: str
    company: str
    location: str
    start_date: str  # "YYYY-MM", se mantiene como texto
    end_date: Optional[str] = None  # None = "Present"
    show: bool = True
    bullets: List[str] = []


class Leadership(BaseModel):
    title: str
    organization: str
    location: Optional[str] = None
    date: str
    description: str
    show: bool = True


class Language(BaseModel):
    name: str
    level: str


class Skills(BaseModel):
    technical: List[str] = []
    laboratory: List[str] = []
    languages: List[Language] = []


class Candidate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    postal_code: Optional[str] = None
    about_me: Optional[str] = None
    education: List[Education] = []
    experience: List[Experience] = []
    leadership: List[Leadership] = []
    skills: Skills = Skills()
    interests: List[str] = []