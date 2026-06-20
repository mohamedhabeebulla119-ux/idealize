from typing import Dict, Any

class CostCalculator:
    """
    CostCalculator computes import duties, VAT, PAL, and total estimated costs
    based on the CIF product value and relevant tax percentages.
    """
    
    @staticmethod
    def calculate_costs(
        product_value: float,
        duty: float,
        vat: float,
        pal: float
    ) -> Dict[str, Any]:
        """
        Calculates cost breakdown.
        
        Args:
            product_value (float): The value of the product (CIF/FOB).
            duty (float): Import duty percentage.
            vat (float): Value Added Tax percentage.
            pal (float): Port and Airport Development Levy percentage.

        Returns:
            Dict[str, Any]: Calculated amounts and estimated total cost.
        """
        # Validate inputs
        val: float = max(0.0, float(product_value))
        d_pct: float = max(0.0, float(duty))
        v_pct: float = max(0.0, float(vat))
        p_pct: float = max(0.0, float(pal))
        
        # Calculations:
        # 1. Port and Airport Development Levy (PAL) Amount
        pal_amount: float = round(val * (p_pct / 100.0), 2)
        
        # 2. Customs Import Duty Amount
        duty_amount: float = round(val * (d_pct / 100.0), 2)
        
        # 3. Value Added Tax (VAT) Amount
        # Base of VAT in Sri Lanka typically adds import duty
        vat_base: float = val + duty_amount
        vat_amount: float = round(vat_base * (v_pct / 100.0), 2)
        
        # 4. Total Cost Calculation
        estimated_total: float = round(val + duty_amount + vat_amount + pal_amount, 2)
        
        return {
            "product_value": val,
            "duty_amount": duty_amount,
            "vat_amount": vat_amount,
            "pal_amount": pal_amount,
            "estimated_total": estimated_total
        }
