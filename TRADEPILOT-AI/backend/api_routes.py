import sys
import os
from fastapi import APIRouter, HTTPException

# Ensure the root directory is in sys.path so we can import agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.compliance_agent import ComplianceAgent
from agents.agency_recommendation_agent import AgencyRecommendationAgent
from agents.workflow_agent import WorkflowAgent
from agents.risk_agent import RiskAgent
from agents.checklist_agent import ChecklistAgent
from agents.document_suggestion_agent import DocumentSuggestionAgent
from agents.cost_advisory_agent import CostAdvisoryAgent

from backend.schemas import TradeScenarioRequest, ChecklistRequest, CostEstimationRequest

router = APIRouter(prefix="/api")

# Initialize agents
compliance_agent = ComplianceAgent()
agency_agent = AgencyRecommendationAgent()
workflow_agent = WorkflowAgent()
risk_agent = RiskAgent()
checklist_agent = ChecklistAgent()
document_suggestion_agent = DocumentSuggestionAgent()
cost_advisory_agent = CostAdvisoryAgent()

@router.post("/compliance")
async def check_compliance(request: TradeScenarioRequest):
    try:
        result = compliance_agent.check_compliance(
            request.trade_type, 
            request.product, 
            request.country
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agencies")
async def recommend_agencies(request: TradeScenarioRequest):
    try:
        result = agency_agent.recommend_agencies(
            request.trade_type, 
            request.product, 
            request.country
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/workflow")
async def generate_workflow(request: TradeScenarioRequest):
    try:
        result = workflow_agent.generate_workflow(
            request.trade_type, 
            request.product, 
            request.country
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/risk")
async def analyze_risks(request: ChecklistRequest):
    try:
        result = risk_agent.analyze_risks(
            request.trade_type,
            request.product,
            request.country,
            request.documents,
            request.approvals
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/checklist")
async def generate_checklist(request: ChecklistRequest):
    try:
        result = checklist_agent.generate_checklist(
            request.trade_type,
            request.product,
            request.documents,
            request.approvals
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents")
async def suggest_documents(request: TradeScenarioRequest):
    try:
        result = document_suggestion_agent.suggest_documents(
            request.trade_type,
            request.product,
            request.country
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cost-estimation")
async def estimate_costs(request: CostEstimationRequest):
    try:
        result = cost_advisory_agent.generate_advisory(
            request.product,
            request.country,
            request.product_value
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
