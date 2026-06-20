from models.response_models import RiskResponse

class RiskService:
    def analyze(self, query: str) -> RiskResponse:
        return RiskResponse(
            risks=[
                {"risk_type": "Tariff Risk", "severity": "Medium", "description": "Subject to variable standard import tariffs."}
            ],
            mitigation_steps=[
                "Leverage FTA agreements to lower duties where applicable."
            ]
        )

risk_service = RiskService()
