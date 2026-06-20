from fastapi import APIRouter
from models.request_models import ComplianceRequest
from models.response_models import ComplianceResponse
from services.compliance_service import compliance_service

router = APIRouter()

@router.post("/", response_model=ComplianceResponse)
async def check_compliance(request: ComplianceRequest):
    return compliance_service.run_checks(request.query)
