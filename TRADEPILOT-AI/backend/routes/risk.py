from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from agents.risk_agent import RiskAgent

router = APIRouter()
agent = RiskAgent()

class RiskRequest(BaseModel):
    trade_type: str
    product: str
    country: str
    documents: List[str]
    approvals: List[str]

@router.post("/")
def analyze_risks(request: RiskRequest):
    if not request.trade_type.strip() or not request.product.strip() or not request.country.strip():
        raise HTTPException(status_code=400, detail="Parameters trade_type, product, and country cannot be empty")
    
    if request.trade_type.lower() not in ["import", "export"]:
        raise HTTPException(status_code=400, detail="trade_type must be either 'import' or 'export'")

    result = agent.analyze_risks(
        trade_type=request.trade_type.lower().strip(),
        product=request.product.strip(),
        country=request.country.strip(),
        documents=request.documents,
        approvals=request.approvals
    )
    return result
