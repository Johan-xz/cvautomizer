import argparse
from pathlib import Path
from src.parsers.candidate_parser import CandidateParser
from src.analyzers.job_offer_analyzer import JobOfferAnalyzer
from src.matching.matcher import CVMatcher
from src.generators.cv_generator import CVGenerator

def main():
    parser = argparse.ArgumentParser(description='CVAutomizer - Genera CV adaptado a oferta')
    parser.add_argument('--candidate', required=True, help='Ruta archivo candidato (YAML)')
    parser.add_argument('--offer', required=True, help='Ruta archivo oferta (JSON)')
    parser.add_argument('--output', default='output/cv_adaptado', help='Ruta salida (sin extensión)')
    
    args = parser.parse_args()
    
    print(f"[*] Cargando candidato: {args.candidate}")
    candidate_parser = CandidateParser(args.candidate)
    candidate = candidate_parser.parse()
    
    print(f"[*] Analizando oferta: {args.offer}")
    offer_analyzer = JobOfferAnalyzer(args.offer)
    offer = offer_analyzer.analyze()
    
    print(f"[*] Calculando match...")
    matcher = CVMatcher(candidate, offer)
    result = matcher.calculate_match()
    
    print(f"[OK] Match: {result['match_percentage']}%")
    
    generator = CVGenerator(candidate, offer, result)
    
    # Generar PDF
    pdf_path = f"{args.output}.pdf"
    print(f"[*] Generando PDF: {pdf_path}")
    generator.generate_pdf(pdf_path)
    
    # Generar análisis
    json_path = f"{args.output}_analisis.json"
    print(f"[*] Generando análisis: {json_path}")
    generator.generate_analysis(json_path)
    
    print(f"[OK] Completado!")
    print(f"     CV: {pdf_path}")
    print(f"     Análisis: {json_path}")

if __name__ == '__main__':
    main()
