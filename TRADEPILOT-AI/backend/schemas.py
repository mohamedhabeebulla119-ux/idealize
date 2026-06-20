from pydantic import BaseModel
from typing import List, Optional

class TradeScenarioRequest(BaseModel):
    trade_type: str
    product: str
    country: str

class ChecklistRequest(TradeScenarioRequest):
    documents: List[str] = []
    approvals: List[str] = []

class CostEstimationRequest(BaseModel):
    product: str
    country: str
    product_value: float
