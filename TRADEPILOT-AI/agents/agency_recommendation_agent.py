import os
import json
from typing import Dict, List, Any
import google.generativeai as genai
from dotenv import load_dotenv

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.retriever import retrieve_context

# Load .env file from project root (parent directory of agents/)
dotenv_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

class AgencyRecommendationAgent:
    """
    AgencyRecommendationAgent recommends relevant government agencies in Sri Lanka
    based on the trade scenario (trade type, product, partner country).
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

    def recommend_agencies(
        self,
        trade_type: str,
        product: str,
        country: str
    ) -> Dict[str, Any]:
        """
        Recommends trade regulatory agencies in Sri Lanka.
        
        Args:
            trade_type (str): Either 'import' or 'export'.
            product (str): The product being traded.
            country (str): The partner origin/destination country.

        Returns:
            Dict[str, Any]: Dictionary containing list of recommended agencies and reasons.
        """
        query = f"What are the government agencies and authorities involved in {trade_type}ing {product} to/from {country}?"
        context = retrieve_context(query)

        prompt: str = f"""
You are an expert Government Agency Recommendation engine.
Identify and recommend the relevant government agencies in Sri Lanka involved in the following trade scenario strictly based on the Regulatory Context below.

Scenario:
Trade Type: {trade_type}
Product: {product}
Partner Country: {country}

--- Regulatory Context ---
{context}
--------------------------

Provide the formal name of each agency (e.g. Sri Lanka Customs, Department of Import and Export Control, Sri Lanka Standards Institution, etc.) and a specific, detailed reason why they are required for this trade activity based ONLY on the Regulatory Context.

CRITICAL RULE: If the Regulatory Context does not list any specific agencies for this product, you must ONLY return "Sri Lanka Customs" with the reason "General customs clearing for all imports/exports." Do not hallucinate other agencies.

You must respond with a single, valid JSON object only matching the schema below. Do not include any markdown formatting, backticks, or extra text.

JSON Schema:
{{
  "agencies": [
    {{
      "name": "Name of Government Agency",
      "reason": "Detailed explanation of their role in this trade activity"
    }}
  ]
}}

If the scenario is invalid or cannot be parsed, return:
{{
  "agencies": [
    {{
      "name": "Sri Lanka Customs",
      "reason": "General customs clearing for all imports/exports."
    }}
  ]
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
            # Fallback response
            return {
                "agencies": [
                    {
                        "name": "Sri Lanka Customs",
                        "reason": f"Required for general customs declaration and processing. (Error: {str(e)})"
                    }
                ]
            }
