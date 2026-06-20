from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from agents.document_verification_agent import DocumentVerificationAgent

router = APIRouter()
agent = DocumentVerificationAgent()

class VerificationRequest(BaseModel):
    required_documents: List[str]
    uploaded_documents: List[str]

@router.post("/")
def verify_documents(request: VerificationRequest):
    if not request.required_documents:
        raise HTTPException(status_code=400, detail="required_documents list cannot be empty")
        
    result = agent.verify_documents(
        required_documents=request.required_documents,
        uploaded_documents=request.uploaded_documents
    )
    return result
