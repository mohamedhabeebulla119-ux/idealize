import os
import json
from typing import Dict, List, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env file from project root (parent directory of agents/) to ensure GEMINI_API_KEY is available
dotenv_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

class ComplianceAgent:
    """
    An Agent designed to parse trade activities and determine compliance needs,
    including required documents, government agencies, and approvals/permits
    specific to Sri Lanka's import and export regulations.
    """
    
    def __init__(self) -> None:
        """
        Initializes the ComplianceAgent, configures the google-generativeai client,
        and instantiates the generative model.
        """
        api_key: str | None = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        # Using the verified working model 'gemini-2.5-flash'
        self.model: genai.GenerativeModel = genai.GenerativeModel('gemini-2.5-flash')

    def check_compliance(self, trade_type: str, product: str, country: str) -> Dict[str, Any]:
        """
        Generates and processes a compliance check for Sri Lanka import/export scenarios.
        
        Args:
            trade_type (str): The trade movement ('import' or 'export').
            product (str): The description or category of the product.
            country (str): The country of origin or destination country.

        Returns:
            Dict[str, Any]: A dictionary containing lists of required documents, 
                            agencies, and approvals/permits.
        """
        # Prompt structured for Sri Lanka trade landscape compliance
        prompt: str = f"""
Analyze the trade compliance requirements for the following scenario under Sri Lanka's trade regulations:
Trade Type: {trade_type}
Product: {product}
Partner Country: {country}

Identify:
1. Required Documents for customs clearance in Sri Lanka (e.g. Commercial Invoice, Packing List, Bill of Lading, Certificate of Origin, etc.).
2. Required Government Agencies in Sri Lanka (e.g. Sri Lanka Customs, Import and Export Control Department, Sri Lanka Standards Institution, Coconut Development Authority, etc.).
3. Required Approvals / Permits from these authorities.

You must respond with a single, valid JSON object only matching the schema below. Do not include any markdown formatting, backticks, or extra text.

JSON Schema:
{{
  "documents": ["doc1", "doc2", ...],
  "agencies": ["agency1", "agency2", ...],
  "approvals": ["approval1", "approval2", ...]
}}

If the query is extremely unclear or invalid, return:
{{
  "documents": [],
  "agencies": [],
  "approvals": [],
  "note": "Unable to determine exact compliance requirements."
}}
"""
        try:
            # Request JSON output structure from Gemini model
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            # Extract and parse the returned JSON string
            result_text: str = response.text.strip()
            data: Dict[str, Any] = json.loads(result_text)
            return data
            
        except Exception as e:
            # Clean fallback dictionary if the API key fails or another exception is thrown
            return {
                "documents": [],
                "agencies": [],
                "approvals": [],
                "note": f"Unable to determine exact compliance requirements. Error: {str(e)}"
            }
