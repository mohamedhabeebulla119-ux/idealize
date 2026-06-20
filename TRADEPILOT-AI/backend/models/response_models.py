from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]

class WorkflowResponse(BaseModel):
    workflow_id: str
    steps: List[Dict[str, Any]]
    compliance_checks: List[Dict[str, Any]]

class ComplianceResponse(BaseModel):
    status: str
    issues: List[Dict[str, Any]]

class RiskResponse(BaseModel):
    risks: List[Dict[str, Any]]
    mitigation_steps: List[str]

class ChecklistResponse(BaseModel):
    items: List[Dict[str, Any]]
