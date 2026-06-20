import os
import json
from typing import Dict, List, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env file from project root (parent directory of agents/)
dotenv_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

class ChecklistAgent:
    """
    ChecklistAgent evaluates user readiness for import/export operations in Sri Lanka.
    It calculates a readiness score, determines status, and generates missing checklist items
    and next steps using the Gemini API.
    """
    
    def __init__(self) -> None:
        """
        Initializes the ChecklistAgent, configuring the Gemini API and initializing the model.
        """
        api_key: str | None = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        # Using verified gemini-2.5-flash model
        self.model: genai.GenerativeModel = genai.GenerativeModel('gemini-2.5-flash')

    def generate_checklist(
        self,
        trade_type: str,
        product: str,
        documents: List[str],
        approvals: List[str]
    ) -> Dict[str, Any]:
        """
        Calculates readiness metrics and builds a checklist of completed and missing tasks.
        
        Args:
            trade_type (str): Either 'import' or 'export'.
            product (str): The product description.
            documents (List[str]): User-provided list of existing documents.
            approvals (List[str]): User-provided list of existing permits/approvals.

        Returns:
            Dict[str, Any]: Dictionary containing readiness_score, status, 
                            completed_items, missing_items, next_actions.
        """
        prompt: str = f"""
Evaluate the trade readiness score, status, completed items, missing items, and next actions for the following Sri Lanka trade scenario:
Trade Type: {trade_type}
Product: {product}
Provided Documents: {json.dumps(documents)}
Provided Approvals/Permits: {json.dumps(approvals)}

Analyze if any essential documents or approvals (e.g. Import Permits, Customs Declarations, specific authority approvals, shipping documents) are missing for this product under Sri Lanka's trade regulations.
Calculate a numeric readiness score from 0 to 100:
- 0 to 49: "Not Ready"
- 50 to 89: "Partially Ready"
- 90 to 100: "Ready"

You must respond with a single, valid JSON object only matching the schema below. Do not include any markdown formatting, backticks, or extra text.

JSON Schema:
{{
  "readiness_score": integer (0 to 100),
  "status": "Ready" or "Partially Ready" or "Not Ready",
  "completed_items": ["item1", "item2", ...],
  "missing_items": ["item1", "item2", ...],
  "next_actions": ["action1", "action2", ...]
}}

If the scenario is invalid or cannot be processed, return:
{{
  "readiness_score": 0,
  "status": "Not Ready",
  "completed_items": [],
  "missing_items": ["Invalid scenario details provided."],
  "next_actions": ["Please re-verify input parameters and try again."]
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
            # Fallback response in case of API or parsing error
            return {
                "readiness_score": 0,
                "status": "Not Ready",
                "completed_items": [],
                "missing_items": [f"Error occurred during checklist evaluation: {str(e)}"],
                "next_actions": ["Check API Key configuration and network connection."]
            }
