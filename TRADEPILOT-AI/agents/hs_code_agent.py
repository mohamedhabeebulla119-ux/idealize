import os
import json
from typing import Dict, Any
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load .env file from project root (parent directory of agents/)
dotenv_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

class HSCodeAgent:
    """
    HSCodeAgent determines the most likely 4-digit HS Code and category for a product description.
    Uses the modern google-genai SDK.
    """
    def __init__(self) -> None:
        api_key: str | None = os.getenv("GEMINI_API_KEY")
        self.client: genai.Client | None = None
        if api_key:
            self.client = genai.Client(api_key=api_key)

    def determine_hs_code(self, product: str) -> Dict[str, Any]:
        """
        Determines HS Code, category name, and confidence score.
        """
        prompt: str = f"""
Determine the most likely 4-digit HS Code and category name for the following product:
Product: {product}

You must respond with a single, valid JSON object only matching the schema below. Do not include any markdown formatting, backticks, or extra text.

JSON Schema:
{{
  "hs_code": "4-digit string code (e.g. 8711)",
  "category": "Category name (e.g. Motorcycles)",
  "confidence": float (0.0 to 1.0)
}}

If the product is completely unrecognizable, return:
{{
  "hs_code": "0000",
  "category": "Unknown",
  "confidence": 0.0
}}
"""
        if not self.client:
            return {
                "hs_code": "0000",
                "category": "Unknown",
                "confidence": 0.0,
                "error": "Gemini API client not configured"
            }

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            text = response.text.strip()
            # Handle possible markdown wrap if output is enclosed
            if text.startswith("```"):
                lines = text.split("\n")
                if lines[0].startswith("```json") or lines[0].startswith("```"):
                    lines = lines[1:-1]
                text = "\n".join(lines).strip()

            data: Dict[str, Any] = json.loads(text)
            return data
        except Exception as e:
            # Under quota limits or network failures, fall back to safe unknowns instead of crashing
            return {
                "hs_code": "0000",
                "category": "Unknown",
                "confidence": 0.0,
                "error": str(e)
            }
