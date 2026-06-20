from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from agents.cost_advisory_agent import CostAdvisoryAgent

router = APIRouter()
agent = CostAdvisoryAgent()

class CostEstimationRequest(BaseModel):
    product: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)
    product_value: float = Field(..., gt=0)

@router.post("/")
def estimate_cost(request: CostEstimationRequest):
    try:
        result = agent.generate_advisory(
            product=request.product.strip(),
            country=request.country.strip(),
            product_value=request.product_value
        )
        return {
            "hs_code": result["hs_code"],
            "category": result["category"],
            "tax_rates": result["tax_rates"],
            "cost_breakdown": result["cost_breakdown"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
