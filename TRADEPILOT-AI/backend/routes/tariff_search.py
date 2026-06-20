from fastapi import APIRouter
from pydantic import BaseModel
from agents.tariff_search_agent import TariffSearchAgent
from backend.cache import cache_manager

router = APIRouter()
agent = TariffSearchAgent()

class TariffSearchRequest(BaseModel):
    product: str
    hs_code: str

@router.post("/")
def search_tariffs(request: TariffSearchRequest):
    cached = cache_manager.get("tariff_search", product=request.product, hs_code=request.hs_code)
    if cached:
        return cached

    result = agent.search_tariff_rates(product=request.product, hs_code=request.hs_code)
    cache_manager.set("tariff_search", result, product=request.product, hs_code=request.hs_code)
    return result
