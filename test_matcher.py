from src.parsers.candidate_parser import CandidateParser
from src.analyzers.job_offer_analyzer import JobOfferAnalyzer
from src.matching.matcher import CVMatcher

# Cargar candidato y oferta
candidate_parser = CandidateParser('data/candidate.yaml')
candidate = candidate_parser.parse()

offer_analyzer = JobOfferAnalyzer('data/job_offer.json')
offer = offer_analyzer.analyze()

# Calcular match
matcher = CVMatcher(candidate, offer)
result = matcher.calculate_match()

print(f"✓ Match: {result['match_percentage']}%")
print(f"  Skills matched: {', '.join(result['matched_skills'])}")
print(f"  Missing skills: {', '.join(result['missing_skills'])}")
