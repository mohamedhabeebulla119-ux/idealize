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

class DocumentSuggestionAgent:
    """
    DocumentSuggestionAgent identifies and recommends all required trade documents
    and their purposes for import and export activities in Sri Lanka.
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

    def suggest_documents(
        self,
        trade_type: str,
        product: str,
        country: str
    ) -> Dict[str, Any]:
        """
        Suggests required trade documents for Sri Lanka trade scenarios.
        
        Args:
            trade_type (str): Either 'import' or 'export'.
            product (str): The product being traded.
            country (str): The partner origin/destination country.

        Returns:
            Dict[str, Any]: Dictionary containing list of required_documents and their purposes.
        """
        # Retrieve context from RAG
        query = f"What are all the required trade documents and their specific regulatory or logistics purposes for {trade_type}ing {product} involving {country}?"
        context = retrieve_context(query)

        prompt: str = f"""
You are an expert Trade Document Analyst.
Identify and suggest all required trade documents and their specific regulatory/logistics purposes for the following trade scenario strictly based on the Regulatory Context below.

Scenario:
Trade Type: {trade_type}
Product: {product}
Partner Country: {country}

--- Regulatory Context ---
{context}
--------------------------

For each document found in the context, provide its formal name (e.g. Commercial Invoice, Packing List, Bill of Lading, Import Control License, Certificate of Origin, etc.) and a concise purpose based ONLY on the context (e.g. Proof of purchase, Cargo details, shipment ownership, regulatory approval, etc.).

CRITICAL RULE: Base the suggested documents and their purposes ONLY on the rules specified in the Regulatory Context. If the context does not specify documents, return an empty array. Do not hallucinate external documents.

You must respond with a single, valid JSON object only matching the schema below. Do not include any markdown formatting, backticks, or extra text.

JSON Schema:
{{
  "required_documents": [
    {{
      "document": "Document Name",
      "purpose": "Brief description of the document's purpose"
    }}
  ]
}}

If the scenario is invalid or cannot be parsed, return:
{{
  "required_documents": [],
  "note": "Unable to determine required documents."
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
                "required_documents": [],
                "note": f"Unable to determine required documents. Error: {str(e)}"
            }
