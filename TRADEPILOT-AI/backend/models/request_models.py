from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    query: str

class WorkflowRequest(BaseModel):
    product_name: str
    origin_country: str
    destination_country: str
    hs_code: Optional[str] = None

class ComplianceRequest(BaseModel):
    query: str

class RiskRequest(BaseModel):
    query: str

class ChecklistRequest(BaseModel):
    query: str
