import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import intent
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
