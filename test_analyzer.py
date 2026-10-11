from src.analyzers.job_offer_analyzer import JobOfferAnalyzer

analyzer = JobOfferAnalyzer('data/job_offer.json')
offer = analyzer.analyze()

print(f"✓ Oferta: {offer.title}")
print(f"  Empresa: {offer.company}")
print(f"  Skills requeridos: {', '.join(offer.required_skills)}")
print(f"  Años experiencia: {offer.experience_years}")
print(f"  Keywords: {', '.join(offer.keywords)}")
