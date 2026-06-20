import os
import json
from typing import Dict, List, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env file from project root (parent directory of agents/)
dotenv_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

class DocumentVerificationAgent:
    """
    DocumentVerificationAgent semantically compares required compliance documents
    against uploaded/provided documents to determine which are present,
    which are missing, and provide action recommendations.
    """
    
    def __init__(self) -> None:
        """
        Initializes the agent and configures the Gemini API client.
        """
        api_key: str | None = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        # Using verified gemini-2.5-flash model
        self.model: genai.GenerativeModel = genai.GenerativeModel('gemini-2.5-flash')

    def verify_documents(
        self,
        required_documents: List[str],
        uploaded_documents: List[str]
    ) -> Dict[str, Any]:
        """
        Compares uploaded documents against compliance required documents.
        
        Args:
            required_documents (List[str]): List of documents required for trade.
            uploaded_documents (List[str]): List of documents provided by the user.

        Returns:
            Dict[str, Any]: Dictionary containing verification_status,
                            missing_documents, available_documents, recommendations.
        """
        prompt: str = f"""
Compare the list of uploaded trade documents against the required compliance documents.
Perform a semantic match (e.g. if 'invoice.pdf' or 'Commercial Invoice' matches 'Commercial Invoice').

Required Documents: {json.dumps(required_documents)}
Uploaded Documents: {json.dumps(uploaded_documents)}

Determine:
1. Available Documents: List of required documents that are successfully matched/provided.
2. Missing Documents: List of required documents that have not been provided or matched.
3. Verification Status: "Complete" if all required documents are provided, otherwise "Incomplete".
4. Recommendations: Actionable steps on how to obtain missing items or verify document validity.

You must respond with a single, valid JSON object only matching the schema below. Do not include any markdown formatting, backticks, or extra text.

JSON Schema:
{{
  "verification_status": "Complete" or "Incomplete",
  "missing_documents": ["doc1", "doc2", ...],
  "available_documents": ["doc1", "doc2", ...],
  "recommendations": ["rec1", "rec2", ...]
}}
"""
        try:
            # Call Gemini and request structured JSON output
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            # Parse response text
            data: Dict[str, Any] = json.loads(response.text.strip())
            return data
        except Exception as e:
            # Fallback error response
            return {
                "verification_status": "Incomplete",
                "missing_documents": required_documents,
                "available_documents": [],
                "recommendations": [
                    f"Error occurred during verification: {str(e)}",
                    "Please check your API key and connection."
                ]
            }
