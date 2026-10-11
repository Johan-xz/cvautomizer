import yaml
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
