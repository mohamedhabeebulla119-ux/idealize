import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add parent project root directory to sys.path to enable 'agents' import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes import intent, workflow, compliance, risk, checklist, document_verification
from config import settings

app = FastAPI(
    title="TradePilot AI API",
    description="Production-ready FastAPI backend skeleton for TradePilot AI",
    version="0.1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
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

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "TradePilot AI"
    }

@app.get("/")
def read_root():
    return {
        "message": "Welcome to TradePilot AI API. Use /health to check status."
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
