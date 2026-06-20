from typing import Dict, Any

# Initial seed for standard tax rules based on HS Code
TAX_RULES: Dict[str, Dict[str, float]] = {
    "8711": {
        "duty": 20.0,
        "vat": 18.0,
        "pal": 10.0
    },
    "8517": {
        "duty": 15.0,
        "vat": 18.0,
        "pal": 5.0
    }
}

class TaxRuleEngine:
    """
    TaxRuleEngine manages and fetches standard tax rates based on 4-digit HS Codes.
    """
    @staticmethod
    def get_tax_rates(hs_code: str) -> Dict[str, float]:
        """
        Fetches the tax rates (duty, vat, pal) for a given HS Code.
        
        Args:
            hs_code (str): The 4-digit HS Code.

        Returns:
            Dict[str, float]: Dictionary containing standard rates. Fallbacks to default rates if not found.
        """
        # Clean the HS Code input
        clean_code: str = str(hs_code).strip()[:4]
        
        # Look up in rules dictionary
        if clean_code in TAX_RULES:
            return TAX_RULES[clean_code]
            
        # Fallback default rates if HS Code is not registered
        return {
            "duty": 10.0,
            "vat": 18.0,
            "pal": 5.0
        }
