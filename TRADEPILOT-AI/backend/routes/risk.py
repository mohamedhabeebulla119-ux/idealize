from fastapi import APIRouter
from models.request_models import RiskRequest
from models.response_models import RiskResponse
from services.risk_service import risk_service

router = APIRouter()

@router.post("/", response_model=RiskResponse)
async def analyze_risks(request: RiskRequest):
    return risk_service.analyze(request.query)
