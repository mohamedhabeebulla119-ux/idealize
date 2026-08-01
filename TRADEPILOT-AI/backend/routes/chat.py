from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict, Optional
from agents.chat_agent import ChatAgent
from pypdf import PdfReader
import io

router = APIRouter()
agent = ChatAgent()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

@router.post("/chat")
def chat(request: ChatRequest):
    try:
        # Convert ChatMessage items to plain dicts for the agent
        history_dicts = [{"role": msg.role, "content": msg.content} for msg in request.history] if request.history else []
        result = agent.chat(
            user_message=request.message,
            history=history_dicts
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        filename = file.filename
        content_bytes = await file.read()
        
        # Determine file type and extract content
        text_content = ""
        if filename.endswith(".pdf"):
            pdf_file = io.BytesIO(content_bytes)
            reader = PdfReader(pdf_file)
            extracted_pages = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_pages.append(text)
            text_content = "\n\n".join(extracted_pages)
        elif filename.endswith((".txt", ".md")):
            text_content = content_bytes.decode("utf-8")
        else:
            raise HTTPException(
                status_code=400, 
                detail="Unsupported file format. Please upload a PDF, TXT, or MD file."
            )

        if not text_content.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract any readable text from the document."
            )

        # Ingest text into vector DB via ChatAgent
        result = agent.ingest_custom_document(filename, text_content)
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result.get("message"))
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
