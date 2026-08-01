import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.retriever import retrieve_context

# Load .env file from project root (parent directory of agents/)
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

class WorkflowAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_workflow(self, trade_type: str, product: str, country: str) -> dict:
        query = f"What is the step-by-step procedure and roadmap for {trade_type}ing {product} to/from {country}?"
        context = retrieve_context(query)

        prompt = f"""
You are an expert Trade Operations Planner.
Generate a realistic, step-by-step global trade workflow roadmap for the following scenario strictly based on the Regulatory Context below.

Scenario:
Trade Type: {trade_type}
Product: {product}
Country: {country}

--- Regulatory Context ---
{context}
--------------------------

CRITICAL RULE: Base the workflow steps ONLY on the provided Regulatory Context. Do not hallucinate external procedures.

You must respond with a single, valid JSON object only matching the schema below. Do not include any markdown formatting, backticks, or extra text.

JSON Schema:
JSON Schema:
{{
  "message": "A helpful, conversational AI introduction explaining the steps.",
  "workflow": [
    {{
      "step": 1,
      "title": "Short descriptive step title"
    }},
    {{
      "step": 2,
      "title": "Next step title"
    }}
  ]
}}
"""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text.strip())
            return data
        except Exception as e:
            # Fallback workflow in case of API issues
            return {
                "message": f"Here is the standard workflow for {trade_type}ing {product}:",
                "workflow": [
                    {"step": 1, "title": f"Verify {trade_type.capitalize()} Eligibility for {product}"},
                    {"step": 2, "title": f"Obtain necessary permits from {country}"},
                    {"step": 3, "title": "Submit Customs Declaration"},
                    {"step": 4, "title": "Settle Duties and Tariffs"}
                ],
                "error": str(e)
            }
