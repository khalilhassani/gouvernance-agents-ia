from fastapi import APIRouter
from ..models.schemas import GlobalReportResponse
from ..tests_engine import engine

router = APIRouter(prefix="/tests", tags=["Tests Engine"])

@router.post("/run", response_model=GlobalReportResponse)
def run_tests():
    """
    Executes the business test suite and returns the report.
    """
    return engine.run_test_suite()

@router.get("/report", response_model=GlobalReportResponse)
def get_report():
    """
    Retrieves the latest generated report.
    """
    return engine.get_latest_report()
