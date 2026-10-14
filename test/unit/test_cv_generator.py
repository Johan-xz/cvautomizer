from src.parsers.candidate_parser import CandidateParser
from src.analyzers.job_offer_analyzer import JobOfferAnalyzer
from src.matching.matcher import CVMatcher
from src.generators.cv_generator import CVGenerator

candidate_parser = CandidateParser('data/candidate.yaml')
candidate = candidate_parser.parse()

offer_analyzer = JobOfferAnalyzer('data/job_offer.json')
offer = offer_analyzer.analyze()

matcher = CVMatcher(candidate, offer)
result = matcher.calculate_match()

generator = CVGenerator(candidate, offer, result)
generator.generate_pdf('output/cv_adaptado.pdf')

print("✓ CV generado: output/cv_adaptado.pdf")
