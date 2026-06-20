from models.response_models import ComplianceResponse

class ComplianceService:
    def run_checks(self, query: str) -> ComplianceResponse:
        return ComplianceResponse(
            status="Compliant",
            issues=[]
        )

compliance_service = ComplianceService()
