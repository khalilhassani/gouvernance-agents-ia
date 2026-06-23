from fastapi import APIRouter
from ..models.schemas import AgentRunRequest, AgentRunResponse
from ..services.agent_service import run_ai_agent

router = APIRouter(prefix="/agents", tags=["Agent"])

@router.post("/run", response_model=AgentRunResponse)
def run_agent(payload: AgentRunRequest):
    """
    Executes the simulated AI Agent on citizen input.
    """
    return run_ai_agent(payload.input_value)
