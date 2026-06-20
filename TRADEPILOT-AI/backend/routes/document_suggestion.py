from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.document_suggestion_agent import DocumentSuggestionAgent
from backend.cache import cache_manager

router = APIRouter()
agent = DocumentSuggestionAgent()

class DocumentSuggestionRequest(BaseModel):
    trade_type: str
    product: str
    country: str

@router.post("/")
def get_document_suggestions(request: DocumentSuggestionRequest):
    cached = cache_manager.get("documents", trade_type=request.trade_type, product=request.product, country=request.country)
    if cached:
        return cached

    result = agent.suggest_documents(
        trade_type=request.trade_type,
        product=request.product,
        country=request.country
    )
    cache_manager.set("documents", result, trade_type=request.trade_type, product=request.product, country=request.country)
    return result
