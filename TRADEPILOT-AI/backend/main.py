from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Ensure backend imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.api_routes import router

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

# Include the modular routes
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "TradePilot AI API is running. Access /docs for Swagger UI."}

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "TradePilot AI"
    }
