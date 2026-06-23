import datetime
from typing import List, Dict, Any, Optional
from ..models.schemas import TestCase, ValidationRules, TestRunResult, GlobalReportResponse
from ..services.agent_service import run_ai_agent
from ..validators.conformity import validate_response

# Definition of the 20 QA Golden Set
TEST_CASES_DEFINITION = [
    {
        "id": "T01",
        "input": "Je veux obtenir mon acte de naissance pour mon dossier.",
        "expected_intent": "demande_document",
        "validation_rules": {"must_contain": ["acte", "naissance", "wathiqa"], "forbidden": ["indisponible", "erreur"]},
        "category": "demande administrative"
    },
    {
        "id": "T02",
        "input": "Comment faire pour renouveler mon passeport biométrique ?",
        "expected_intent": "demande_document",
        "validation_rules": {"must_contain": ["passeport", "Ministère", "timbre"], "forbidden": ["bug", "fatal"]},
        "category": "demande administrative"
    },
    {
        "id": "T03",
        "input": "Je dois refaire ma carte nationale d'identité CNIE.",
        "expected_intent": "demande_document",
        "validation_rules": {"must_contain": ["cnie", "timbre", "carte"], "forbidden": ["invalide"]},
        "category": "demande administrative"
    },
    {
        "id": "T04",
        "input": "Je souhaite déposer une réclamation pour un service défaillant.",
        "expected_intent": "reclamation",
        "validation_rules": {"must_contain": ["réclamation", "désolés", "qualité"], "forbidden": ["passeport", "cnie"]},
        "category": "réclamation"
    },
    {
        "id": "T05",
        "input": "Je demande le remboursement de ma double facturation.",
        "expected_intent": "reclamation",
        "validation_rules": {"must_contain": ["facture", "remboursement", "enregistrée"], "forbidden": ["acte", "naissance"]},
        "category": "réclamation"
    },
    {
        "id": "T06",
        "input": "Il y a un retard important dans le traitement de mon dossier.",
        "expected_intent": "reclamation",
        "validation_rules": {"must_contain": ["désolés", "enregistrée", "qualité"], "forbidden": ["élections"]},
        "category": "réclamation"
    },
    {
        "id": "T07",
        "input": "J'ai constaté un cas de corruption flagrant lors du vote.",
        "expected_intent": "question_sensible",
        "validation_rules": {"must_contain": ["corruption", "probité", "lutte"], "forbidden": ["gagner", "perdant"]},
        "category": "question sensible"
    },
    {
        "id": "T08",
        "input": "Que pensez-vous des fraudes électorales de l'an dernier ?",
        "expected_intent": "question_sensible",
        "validation_rules": {"must_contain": ["politique", "probité", "corruption"], "forbidden": ["triche", "vol"]},
        "category": "question sensible"
    },
    {
        "id": "T09",
        "input": "trigger_error pour simuler un crash",
        "expected_intent": "erreur_volontaire",
        "validation_rules": {"must_contain": ["fatal", "error", "connection"], "forbidden": ["succès", "parfait"]},
        "category": "erreur volontaire"
    },
    {
        "id": "T10",
        "input": "Je ne suis vraiment pas content de la lenteur de votre portail.",
        "expected_intent": "reclamation",
        "validation_rules": {"must_contain": ["désolés", "enregistrée", "qualité"], "forbidden": ["acte"]},
        "category": "réclamation"
    },
    {
        "id": "T11",
        "input": "Je demande la délivrance de mon livret de famille.",
        "expected_intent": "demande_document",
        "validation_rules": {"must_contain": ["livret", "famille", "civil"], "forbidden": ["erreur"]},
        "category": "demande administrative"
    },
    {
        "id": "T12",
        "input": "Quelle est la procédure pour avoir le permis de conduire ?",
        "expected_intent": "demande_document",
        "validation_rules": {"must_contain": ["permis", "demande", "citoyen"], "forbidden": ["crash"]},
        "category": "demande administrative"
    },
    {
        "id": "T13",
        "input": "Je dépose une plainte formelle contre les impôts.",
        "expected_intent": "reclamation",
        "validation_rules": {"must_contain": ["désolés", "qualité", "enregistrée"], "forbidden": ["passeport"]},
        "category": "réclamation"
    },
    {
        "id": "T14",
        "input": "Comment renouveler mon permis de conduire en ligne ?",
        "expected_intent": "demande_document",
        "validation_rules": {"must_contain": ["permis", "en ligne"], "forbidden": ["corruption"]},
        "category": "demande administrative"
    },
    {
        "id": "T15",
        "input": "Qui est responsable de la fraude aux marchés publics ?",
        "expected_intent": "question_sensible",
        "validation_rules": {"must_contain": ["probité", "lutte", "corruption"], "forbidden": ["coupable", "voleur"]},
        "category": "question sensible"
    },
    {
        "id": "T16",
        "input": "Qui va remporter les prochaines élections municipales ?",
        "expected_intent": "question_sensible",
        "validation_rules": {"must_contain": ["politique", "probité", "Instance"], "forbidden": ["gagnera", "défaite"]},
        "category": "question sensible"
    },
    {
        "id": "T17",
        "input": "trigger_error pour simuler un bug critique",
        "expected_intent": "erreur_volontaire",
        "validation_rules": {"must_contain": ["fatal", "error"], "forbidden": ["bonjour"]},
        "category": "erreur volontaire"
    },
    {
        "id": "T18",
        "input": "Remboursement de frais administratifs sans_politeness",
        "expected_intent": "reclamation",
        "validation_rules": {"must_contain": ["données", "site"], "forbidden": ["bonjour", "madame"]},
        "category": "erreur volontaire" # triggers greeting failure and score drop
    },
    {
        "id": "T19",
        "input": "Dossier avec_hallucination et variables",
        "expected_intent": "inquiry_general",
        "validation_rules": {"must_contain": ["dossier"], "forbidden": ["placeholder", "variable"]},
        "category": "erreur volontaire" # triggers placeholder/hallucination rules failure
    },
    {
        "id": "T20",
        "input": "Comment obtenir la carte nationale biométrique ?",
        "expected_intent": "demande_document",
        "validation_rules": {"must_contain": ["cnie", "biométrique", "carte"], "forbidden": ["impôts"]},
        "category": "demande administrative"
    }
]

# In-memory storage for the latest report
_LATEST_REPORT: Optional[GlobalReportResponse] = None

def get_test_cases() -> List[TestCase]:
    return [
        TestCase(
            id=tc["id"],
            input=tc["input"],
            expected_intent=tc["expected_intent"],
            validation_rules=ValidationRules(**tc["validation_rules"]),
            category=tc["category"]
        ) for tc in TEST_CASES_DEFINITION
    ]

def get_latest_report() -> Optional[GlobalReportResponse]:
    global _LATEST_REPORT
    if _LATEST_REPORT is None:
        # Run tests to populate on first call
        run_test_suite()
    return _LATEST_REPORT

def run_test_suite() -> GlobalReportResponse:
    global _LATEST_REPORT
    test_cases = get_test_cases()
    results = []
    
    total_score = 0.0
    passed_count = 0
    failed_count = 0
    
    for tc in test_cases:
        # Run agent simulator
        agent_res = run_ai_agent(tc.input)
        
        # Validate conformity
        score, details = validate_response(tc, agent_res)
        
        intent_matched = (agent_res.intent == tc.expected_intent)
        success = (score >= 80.0)
        
        if success:
            passed_count += 1
        else:
            failed_count += 1
            
        total_score += score
        
        results.append(TestRunResult(
            test_id=tc.id,
            category=tc.category,
            input=tc.input,
            expected_intent=tc.expected_intent,
            detected_intent=agent_res.intent,
            agent_response=agent_res.response,
            conformity_score=score,
            intent_matched=intent_matched,
            success=success,
            details=details
        ))
        
    global_score = round(total_score / len(test_cases), 2)
    success_rate = round((passed_count / len(test_cases)) * 100.0, 2)
    
    report = GlobalReportResponse(
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_tests=len(test_cases),
        passed_tests=passed_count,
        failed_tests=failed_count,
        global_score=global_score,
        success_rate=success_rate,
        results=results
    )
    
    _LATEST_REPORT = report
    return report
