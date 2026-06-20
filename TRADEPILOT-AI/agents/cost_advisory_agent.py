import os
import sys
from typing import Dict, Any

# Ensure parent directory is in sys.path when running independently
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.hs_code_agent import HSCodeAgent
from agents.tariff_search_agent import TariffSearchAgent

# Import services from backend since uvicorn runs from TRADEPILOT-AI/backend/
try:
    from services.tax_rule_engine import TaxRuleEngine, TAX_RULES
    from services.cost_calculator import CostCalculator
except ImportError:
    # Fallback for alternative python path configurations
    from backend.services.tax_rule_engine import TaxRuleEngine, TAX_RULES
    from backend.services.cost_calculator import CostCalculator

class CostAdvisoryAgent:
    """
    CostAdvisoryAgent coordinates the workflow to estimate import costs:
    1. Resolve product name to HS Code
    2. Lookup tax rates (locally from database, or via web search grounding if missing)
    3. Calculate total breakdown
    4. Compile summary
    """
    
    def __init__(self) -> None:
        self.hs_agent: HSCodeAgent = HSCodeAgent()
        self.search_agent: TariffSearchAgent = TariffSearchAgent()

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
            
            # 2. Get Tax Rates from predefined rules or live search
            clean_code: str = str(hs_code).strip()[:4]
            
            if clean_code in TAX_RULES:
                # Predefined in database
                rates = TAX_RULES[clean_code].copy()
                rates["source"] = "local_database"
                print(f"[CostAdvisoryAgent] Found predefined tax rates locally for HS Code {clean_code}: {rates}")
            else:
                # Missing in database - fetch via live Google Search grounding
                print(f"[CostAdvisoryAgent] HS Code {clean_code} not in database. Fetching live rates...")
                rates = self.search_agent.search_tariff_rates(product, hs_code)
            
            # 3. Calculate Cost Breakdown
            breakdown: Dict[str, Any] = CostCalculator.calculate_costs(
                product_value=product_value,
                duty=rates["duty"],
                vat=rates["vat"],
                pal=rates["pal"]
            )
            
            # Append source of rates info
            rates_source = rates.get("source", "web_search")
            
            return {
                "hs_code": hs_code,
                "category": category,
                "tax_rates": {
                    "duty": rates["duty"],
                    "vat": rates["vat"],
                    "pal": rates["pal"],
                    "source": rates_source
                },
                "cost_breakdown": breakdown,
                "summary": f"Estimated import cost breakdown generated successfully using {rates_source} rates for {product} from {country}."
            }
        except Exception as e:
            return {
                "hs_code": "0000",
                "category": "Unknown",
                "tax_rates": {"duty": 10.0, "vat": 18.0, "pal": 5.0, "source": "fallback_error"},
                "cost_breakdown": {
                    "product_value": product_value,
                    "duty_amount": 0.0,
                    "vat_amount": 0.0,
                    "pal_amount": 0.0,
                    "estimated_total": product_value
                },
                "summary": f"Failed to generate cost breakdown. Error: {str(e)}"
            }
