import datetime
from fastapi import APIRouter
from ..models.schemas import WorkflowExport
from ..tests_engine import engine

router = APIRouter(prefix="/workflow", tags=["Workflow"])

@router.post("/export", response_model=WorkflowExport)
def export_workflow():
    """
    Exports the workflow structure, including agents, tests, validation rules and execution status.
    """
    test_cases = engine.get_test_cases()
    report = engine.get_latest_report()
    
    # Format rules summary
    rules_summary = {
        "total_rules": sum(len(tc.validation_rules.must_contain) + len(tc.validation_rules.forbidden) for tc in test_cases),
        "categories_tested": list(set(tc.category for tc in test_cases))
    }
    
    return WorkflowExport(
        workflow_name="Validation des Agents IA - Atelier Pratique",
        version="1.0.0",
        agents=[
            {
                "name": "CitizenAgent",
                "role": "Interface citoyenne",
                "models": ["llama-3.1-8b-instant"],
                "status": "ACTIVE"
            },
            {
                "name": "SupervisorAgent",
                "role": "Superviseur de conformité et routage",
                "models": ["llama-3.3-70b-versatile"],
                "status": "ACTIVE"
            }
        ],
        test_cases=test_cases,
        validation_rules_summary=rules_summary
    )
