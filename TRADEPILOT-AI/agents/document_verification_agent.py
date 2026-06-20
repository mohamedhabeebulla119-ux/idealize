import os
import json
from typing import Dict, Any
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load .env file from project root
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

class DocumentVerificationAgent:
    """
    Multimodal DocumentVerificationAgent uses Gemini Vision to read physical
    uploaded files (PDFs, Images) and verify they meet strict compliance standards.
    """
    
    def __init__(self) -> None:
        """
        Initializes the agent and configures the new Gemini API client.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        if api_key:
            self.client = genai.Client(api_key=api_key)

    def verify_document_vision(
        self,
        document_type: str,
        expected_standards: str,
        file_bytes: bytes,
        mime_type: str
    ) -> Dict[str, Any]:
        """
        Reads the physical document and checks it against compliance standards.
        """
        if not self.client:
            return {
                "is_valid": False,
                "extracted_data": {},
                "errors": ["API Key missing. Cannot verify document."]
            }
            
        prompt = f"""
You are a highly meticulous Sri Lankan Customs Compliance Auditor.
I have uploaded a physical document of type: "{document_type}".

Your task is to carefully read and analyze the uploaded document.
Check it against the following expected standards:
{expected_standards}

Determine:
1. Is the document valid and fully compliant with the expected standards?
2. Extract the key data points from the document (e.g. Invoice Number, Date, Total Value, etc).
3. If it is NOT valid, list the specific errors (e.g. "Missing Signature", "Date is expired").

You must respond with a single, valid JSON object only matching the schema below.

JSON Schema:
{{
  "is_valid": true or false,
  "extracted_data": {{"key": "value"}},
  "errors": ["error 1", "error 2"]
}}
"""
        try:
            # Create the multimodal part
            doc_part = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt, doc_part],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            text = response.text.strip()
            # Clean markdown if present
            if text.startswith("```"):
                lines = text.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:-1]
                text = "\n".join(lines).strip()
                
            return json.loads(text)
            
        except Exception as e:
            return {
                "is_valid": False,
                "extracted_data": {},
                "errors": [f"Error occurred during OCR vision processing: {str(e)}"]
            }
