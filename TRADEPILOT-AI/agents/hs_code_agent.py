import os
import json
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env file from project root (parent directory of agents/)
dotenv_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

class HSCodeAgent:
    """
    HSCodeAgent determines the most likely 4-digit HS Code and category for a product description.
    """
    def __init__(self) -> None:
        api_key: str | None = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        self.model: genai.GenerativeModel = genai.GenerativeModel('gemini-2.5-flash')

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
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data: Dict[str, Any] = json.loads(response.text.strip())
            return data
        except Exception as e:
            return {
                "hs_code": "0000",
                "category": "Unknown",
                "confidence": 0.0,
                "error": str(e)
            }
