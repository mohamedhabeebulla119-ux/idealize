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

class RiskAgent:
    """
    RiskAgent evaluates global trade scenarios for Sri Lanka, analyzing
    provided documents and approvals to calculate risk levels (Low, Medium, High),
    identify specific operational/regulatory risks, and offer mitigation recommendations.
    """
    
    def __init__(self) -> None:
        """
        Initializes the RiskAgent, configuring the Gemini API and initializing the model.
        """
        api_key: str | None = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        # Using verified gemini-2.5-flash model
        self.model: genai.GenerativeModel = genai.GenerativeModel('gemini-2.5-flash')

    def analyze_risks(
        self,
        trade_type: str,
        product: str,
        country: str,
        documents: List[str],
        approvals: List[str]
    ) -> Dict[str, Any]:
        """
        Analyzes compliance, timeline, and operational risks for the given scenario.
        
        Args:
            trade_type (str): Either 'import' or 'export'.
            product (str): The product description.
            country (str): The partner origin/destination country.
            documents (List[str]): User-provided list of existing documents.
            approvals (List[str]): User-provided list of existing permits/approvals.

        Returns:
            Dict[str, Any]: Dictionary containing risk_level, risks, and recommendations.
        """
        # Retrieve context from RAG
        query = f"What are the common risks, delays, holds, and required documents for {trade_type}ing {product} involving {country}?"
        context = retrieve_context(query)

        prompt: str = f"""
You are an expert Trade Risk Analyst.
Evaluate the global trade risk level, specific risks, and recommendations for the following scenario strictly based on the Regulatory Context below.

Scenario:
Trade Type: {trade_type}
Product: {product}
Partner Country: {country}
Provided Documents: {json.dumps(documents)}
Provided Approvals/Permits: {json.dumps(approvals)}

--- Regulatory Context ---
{context}
--------------------------

Analyze if any essential documents or approvals (like Import Permits from Import & Export Control Department, Customs Declarations, special authority approvals, or shipping documents) are missing.
Estimate the potential for customs delays, tariff disputes, or certification holds based on the provided list compared to the Regulatory Context.

CRITICAL RULE: If the Regulatory Context does not contain enough information to determine the risks, state "Unable to determine risks based on current regulations" in the risks array, and set risk_level to "Medium".

You must respond with a single, valid JSON object only matching the schema below. Do not include any markdown formatting, backticks, or extra text.

JSON Schema:
{
  "message": "A helpful, conversational AI introduction summarizing the risk profile.",
  "risks": [
    {
      "type": "e.g., Regulatory, Financial, Logistics, Operational",
      "description": "Specific details about the risk based on the context",
      "severity": "High, Medium, or Low",
      "mitigation": "Actionable advice to minimize this risk"
    }
  ]
}

If the scenario is invalid or cannot be processed, return:
{
  "message": "Unable to process the request.",
  "risks": [{"type": "Error", "description": "Unable to determine compliance risks due to invalid scenario parameters.", "severity": "High", "mitigation": "Re-verify all scenario inputs and documents list."}]
}
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
                "message": "An error occurred during analysis.",
                "risks": [
                    {
                        "type": "System",
                        "description": f"Error occurred during risk evaluation: {str(e)}",
                        "severity": "High",
                        "mitigation": "Check API Key configuration and network connection."
                    }
                ]
            }
