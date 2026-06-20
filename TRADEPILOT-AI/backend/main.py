import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import query, workflow, compliance, risk, checklist
from config import settings

app = FastAPI(
    title="TradePilot AI API",
    description="Backend services for TradePilot AI trade compliance platform",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(query.router, prefix="/api/query", tags=["Query"])
app.include_router(workflow.router, prefix="/api/workflow", tags=["Workflow"])
app.include_router(compliance.router, prefix="/api/compliance", tags=["Compliance"])
app.include_router(risk.router, prefix="/api/risk", tags=["Risk"])
app.include_router(checklist.router, prefix="/api/checklist", tags=["Checklist"])

@app.get("/")
def read_root():
    return {"message": "Welcome to TradePilot AI API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
