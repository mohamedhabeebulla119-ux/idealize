import os
import sys
from typing import Dict, Any

# Ensure parent directory is in sys.path when running independently
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.hs_code_agent import HSCodeAgent
# Import services from backend since uvicorn runs from TRADEPILOT-AI/backend/
try:
    from services.tax_rule_engine import TaxRuleEngine
    from services.cost_calculator import CostCalculator
except ImportError:
    # Fallback for alternative python path configurations
    from backend.services.tax_rule_engine import TaxRuleEngine
    from backend.services.cost_calculator import CostCalculator

class CostAdvisoryAgent:
    """
    CostAdvisoryAgent coordinates the workflow to estimate import costs:
    1. Resolve product name to HS Code
    2. Lookup tax rates
    3. Calculate total breakdown
    4. Compile summary
    """
    
    def __init__(self) -> None:
        self.hs_agent: HSCodeAgent = HSCodeAgent()

    def generate_advisory(
        self,
        product: str,
        country: str,
        product_value: float
    ) -> Dict[str, Any]:
        """
        Coordinates HS code retrieval, tax lookup, and cost calculation.
        """
        try:
            # 1. Get HS Code
            hs_info: Dict[str, Any] = self.hs_agent.determine_hs_code(product)
            hs_code: str = hs_info.get("hs_code", "0000")
            category: str = hs_info.get("category", "Unknown")
            
            # 2. Get Tax Rates from Engine
            rates: Dict[str, float] = TaxRuleEngine.get_tax_rates(hs_code)
            
            # 3. Calculate Cost Breakdown
            breakdown: Dict[str, Any] = CostCalculator.calculate_costs(
                product_value=product_value,
                duty=rates["duty"],
                vat=rates["vat"],
                pal=rates["pal"]
            )
            
            return {
                "hs_code": hs_code,
                "category": category,
                "tax_rates": rates,
                "cost_breakdown": breakdown,
                "summary": f"Estimated import cost breakdown generated successfully for {product} from {country}."
            }
        except Exception as e:
            return {
                "hs_code": "0000",
                "category": "Unknown",
                "tax_rates": {"duty": 10.0, "vat": 18.0, "pal": 5.0},
                "cost_breakdown": {
                    "product_value": product_value,
                    "duty_amount": 0.0,
                    "vat_amount": 0.0,
                    "pal_amount": 0.0,
                    "estimated_total": product_value
                },
                "summary": f"Failed to generate cost breakdown. Error: {str(e)}"
            }
