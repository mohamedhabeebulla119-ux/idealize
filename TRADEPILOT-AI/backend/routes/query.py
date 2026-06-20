from fastapi import APIRouter
from models.request_models import QueryRequest
from models.response_models import QueryResponse
from services.gemini_service import gemini_service
from services.rag_service import rag_service

router = APIRouter()

@router.post("/", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    context = rag_service.retrieve(request.query)
    answer = gemini_service.generate_answer(request.query, context)
    return QueryResponse(answer=answer, sources=[{"source": c.get("metadata", {}).get("source", "unknown")} for c in context])
