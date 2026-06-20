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
def get_workflow(request: WorkflowRequest):
    cached = cache_manager.get("workflow", trade_type=request.trade_type, product=request.product, country=request.country)
    if cached:
        return cached
        
    result = agent.generate_workflow(
        trade_type=request.trade_type,
        product=request.product,
        country=request.country
    )
    cache_manager.set("workflow", result, trade_type=request.trade_type, product=request.product, country=request.country)
    return result
