import os
import json
import pytest
import sys

# Ensure backend root is in PATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from backend.app.tests_engine import engine

def test_ai_agent_conformity_score():
    """
    Executes the 20 test cases and checks that the global compliance score exceeds 80%.
    Generates a JSON report in the reports/ directory.
    """
    print("\nLancement de la suite de tests métiers...")
    report = engine.run_test_suite()
    
    # Save JSON report
    report_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "reports"))
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, "validation_report.json")
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report.model_dump(), f, indent=2, ensure_ascii=False)
        
    print(f"Rapport JSON enregistré sous : {report_path}")
    print(f"Nombre total de tests : {report.total_tests}")
    print(f"Tests conformes : {report.passed_tests}")
    print(f"Tests défaillants : {report.failed_tests}")
    print(f"Taux de réussite : {report.success_rate}%")
    print(f"Score de conformité global : {report.global_score}%")
    
    # Assert compliance threshold
    assert report.global_score >= 80.0, f"Échec de la validation : Le score global ({report.global_score}%) est inférieur au seuil de 80%."
    print("✓ Validation réussie avec succès (Score >= 80%).")
