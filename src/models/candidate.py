from pydantic import BaseModel, ValidationInfo, field_validator, model_validator
from typing import List, Optional

from src.utils.dates import es_fecha_valida


def _validar_fecha(valor: Optional[str], info: ValidationInfo) -> Optional[str]:
    if valor is None:
        return valor
    if not es_fecha_valida(valor):
        raise ValueError(
            f"'{info.field_name}' debe tener formato YYYY-MM o YYYY-MM-DD, "
            f"recibido: {valor!r}"
        )
    return valor


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
    start_date: str
    end_date: Optional[str] = None
    show: bool = True
    bullets: List[str] = []

    @field_validator("start_date", "end_date")
    @classmethod
    def formato_fecha(cls, valor, info: ValidationInfo):
        return _validar_fecha(valor, info)

    @model_validator(mode="after")
    def fin_no_antes_de_inicio(self):
        if self.end_date and self.end_date[:7] < self.start_date[:7]:
            raise ValueError("end_date no puede ser anterior a start_date")
        return self


class Leadership(BaseModel):
    title: str
    organization: str
    location: Optional[str] = None
    date: str
    description: str
    show: bool = True

    @field_validator("date")
    @classmethod
    def formato_fecha(cls, valor, info: ValidationInfo):
        return _validar_fecha(valor, info)


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