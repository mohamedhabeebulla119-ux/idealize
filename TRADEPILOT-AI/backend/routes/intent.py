from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.intent_agent import IntentAgent

router = APIRouter()
agent = IntentAgent()

class QueryRequest(BaseModel):
    query: str

@router.post("/")
def analyze_intent(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    result = agent.analyze(request.query)
    return result
