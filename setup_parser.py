#!/usr/bin/env python3
from pathlib import Path

# Crear directorios
Path('src/models').mkdir(parents=True, exist_ok=True)
Path('src/parsers').mkdir(parents=True, exist_ok=True)
Path('data').mkdir(parents=True, exist_ok=True)

# Crear __init__.py
Path('src/__init__.py').touch()
Path('src/models/__init__.py').touch()
Path('src/parsers/__init__.py').touch()

# Crear candidate.py
candidate_py = '''from pydantic import BaseModel
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
'''

Path('src/models/candidate.py').write_text(candidate_py)

# Crear candidate_parser.py
parser_py = '''import yaml
import json
from pathlib import Path
from src.models.candidate import Candidate

class CandidateParser:
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
    
    def parse(self) -> Candidate:
        if self.filepath.suffix == '.yaml':
            return self._parse_yaml()
        elif self.filepath.suffix == '.json':
            return self._parse_json()
        else:
            raise ValueError("Solo YAML o JSON")
    
    def _parse_yaml(self) -> Candidate:
        with open(self.filepath) as f:
            data = yaml.safe_load(f)
        return Candidate(**data)
    
    def _parse_json(self) -> Candidate:
        with open(self.filepath) as f:
            data = json.load(f)
        return Candidate(**data)
'''

Path('src/parsers/candidate_parser.py').write_text(parser_py)

# Crear main.py
main_py = '''from src.parsers.candidate_parser import CandidateParser

parser = CandidateParser('data/candidate.yaml')
candidate = parser.parse()

print(f"✓ Candidato: {candidate.name}")
print(f"  Email: {candidate.email}")
print(f"  Experiencias: {len(candidate.experience)}")
print(f"  Skills: {len(candidate.skills)}")
'''

Path('src/main.py').write_text(main_py)

# Crear candidate.yaml
yaml_data = '''name: Johan Gloria
email: johanglgzz@gmail.com
experience:
  - title: Backend Developer
    company: TechCorp
    start: 2023-01-15
    end: 2024-06-30
    description: APIs en Python
  - title: Junior Dev
    company: Startup
    start: 2022-06-01
    end: 2022-12-31
    description: Automatización
skills:
  - name: Python
    level: senior
  - name: Docker
    level: mid
education:
  - degree: Licenciatura
    school: Universidad
    year: 2022
'''

Path('data/candidate.yaml').write_text(yaml_data)

print("✓ Estructura creada exitosamente")
