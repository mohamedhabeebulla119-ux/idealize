from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.workflow_agent import WorkflowAgent

router = APIRouter()
agent = WorkflowAgent()

class WorkflowRequest(BaseModel):
    trade_type: str
    product: str
    country: str

@router.post("/")
def generate_workflow(request: WorkflowRequest):
    if not request.trade_type or not request.product or not request.country:
        raise HTTPException(status_code=400, detail="Missing required parameters: trade_type, product, or country")
    
    if request.trade_type.lower() not in ["import", "export"]:
        raise HTTPException(status_code=400, detail="trade_type must be either 'import' or 'export'")

    result = agent.generate_workflow(
        trade_type=request.trade_type,
        product=request.product,
        country=request.country
    )
    return result
