from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.compliance_agent import ComplianceAgent

router = APIRouter()
agent = ComplianceAgent()

class ComplianceRequest(BaseModel):
    trade_type: str
    product: str
    country: str

@router.post("/")
def check_compliance(request: ComplianceRequest):
    # Validate that none of the inputs are empty strings or whitespace
    if not request.trade_type.strip() or not request.product.strip() or not request.country.strip():
        raise HTTPException(status_code=400, detail="Parameters trade_type, product, and country cannot be empty")
    
    # Restrict trade_type to allowed values
    if request.trade_type.lower() not in ["import", "export"]:
        raise HTTPException(status_code=400, detail="trade_type must be either 'import' or 'export'")

    # Run the compliance agent verification
    result = agent.check_compliance(
        trade_type=request.trade_type.lower().strip(),
        product=request.product.strip(),
        country=request.country.strip()
    )
    
    return result
