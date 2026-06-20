from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from agents.tariff_search_agent import TariffSearchAgent

router = APIRouter()
agent = TariffSearchAgent()

class TariffSearchRequest(BaseModel):
    product: str = Field(..., min_length=1)
    hs_code: str = Field(..., min_length=1)

@router.post("/")
def search_tariffs(request: TariffSearchRequest):
    try:
        result = agent.search_tariff_rates(
            product=request.product.strip(),
            hs_code=request.hs_code.strip()
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
