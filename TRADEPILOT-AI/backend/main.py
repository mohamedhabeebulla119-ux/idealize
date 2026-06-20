from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Ensure backend imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.routes import intent, workflow, compliance, risk, checklist, document_verification, agency_recommendation, cost, document_suggestion, tariff_search
from backend.config import settings

app = FastAPI(
    title="TradePilot AI Backend",
    description="RAG-powered Multi-Agent API for Sri Lanka Trade Compliance",
    version="1.0.0"
)

# CORS configuration to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(intent.router, prefix="/api/intent", tags=["Intent"])
app.include_router(workflow.router, prefix="/api/workflow", tags=["Workflow"])
app.include_router(compliance.router, prefix="/api/compliance", tags=["Compliance"])
app.include_router(risk.router, prefix="/api/risk", tags=["Risk"])
app.include_router(checklist.router, prefix="/api/checklist", tags=["Checklist"])
app.include_router(document_verification.router, prefix="/api/document-verification", tags=["Document Verification"])
app.include_router(agency_recommendation.router, prefix="/api/agency-recommendation", tags=["Agency Recommendation"])
app.include_router(cost.router, prefix="/api/cost-estimation", tags=["Cost Estimation"])
app.include_router(document_suggestion.router, prefix="/api/documents", tags=["Document Suggestion"])
app.include_router(tariff_search.router, prefix="/api/tariff-search", tags=["Tariff Search"])

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "TradePilot AI"
    }

@app.get("/")
async def root():
    return {"message": "TradePilot AI API is running. Access /docs for Swagger UI."}
