from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.agency_recommendation_agent import AgencyRecommendationAgent

router = APIRouter()
agent = AgencyRecommendationAgent()

class AgencyRecommendationRequest(BaseModel):
    trade_type: str
    product: str
    country: str

@router.post("/")
def recommend_agencies(request: AgencyRecommendationRequest):
    if not request.trade_type.strip() or not request.product.strip() or not request.country.strip():
        raise HTTPException(status_code=400, detail="Parameters trade_type, product, and country cannot be empty")
        
    if request.trade_type.lower() not in ["import", "export"]:
        raise HTTPException(status_code=400, detail="trade_type must be either 'import' or 'export'")

    result = agent.recommend_agencies(
        trade_type=request.trade_type.lower().strip(),
        product=request.product.strip(),
        country=request.country.strip()
    )
    return result
