from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.compliance_agent import ComplianceAgent
from backend.cache import cache_manager

router = APIRouter()
agent = ComplianceAgent()

class ComplianceRequest(BaseModel):
    trade_type: str
    product: str
    country: str

@router.post("/")
def check_compliance(request: ComplianceRequest):
    cached = cache_manager.get("compliance", trade_type=request.trade_type, product=request.product, country=request.country)
    if cached:
        return cached

    result = agent.check_compliance(
        trade_type=request.trade_type.lower().strip(),
        product=request.product.strip(),
        country=request.country.strip()
    )
    cache_manager.set("compliance", result, trade_type=request.trade_type, product=request.product, country=request.country)
    return result
