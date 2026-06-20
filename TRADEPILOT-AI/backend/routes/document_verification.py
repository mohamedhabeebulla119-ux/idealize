from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from agents.document_verification_agent import DocumentVerificationAgent

router = APIRouter()
agent = DocumentVerificationAgent()

@router.post("/")
async def verify_document_vision(
    document_type: str = Form(...),
    expected_standards: str = Form(...),
    file: UploadFile = File(...)
):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
        
    # Read the raw bytes into memory
    file_bytes = await file.read()
    mime_type = file.content_type
    
    if not mime_type:
        mime_type = "application/octet-stream"
        
    result = agent.verify_document_vision(
        document_type=document_type,
        expected_standards=expected_standards,
        file_bytes=file_bytes,
        mime_type=mime_type
    )
    return result
