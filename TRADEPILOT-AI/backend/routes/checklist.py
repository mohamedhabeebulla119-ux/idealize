from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from agents.checklist_agent import ChecklistAgent

router = APIRouter()
agent = ChecklistAgent()

class ChecklistRequest(BaseModel):
    trade_type: str
    product: str
    documents: List[str]
    approvals: List[str]

@router.post("/")
def generate_checklist(request: ChecklistRequest):
    if not request.trade_type.strip() or not request.product.strip():
        raise HTTPException(status_code=400, detail="Parameters trade_type and product cannot be empty")
    
    if request.trade_type.lower() not in ["import", "export"]:
        raise HTTPException(status_code=400, detail="trade_type must be either 'import' or 'export'")

    result = agent.generate_checklist(
        trade_type=request.trade_type.lower().strip(),
        product=request.product.strip(),
        documents=request.documents,
        approvals=request.approvals
    )
    return result
