from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.intent_agent import IntentAgent

router = APIRouter()
agent = IntentAgent()

class QueryRequest(BaseModel):
    query: str

from backend.cache import cache_manager

@router.post("/")
def analyze_intent(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    cached = cache_manager.get("intent", query=request.query)
    if cached:
        return cached
        
    result = agent.process(request.query)
    cache_manager.set("intent", result, query=request.query)
    return result
