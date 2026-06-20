import json
import google.generativeai as genai
from config import settings

class IntentAgent:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def analyze(self, query: str) -> dict:
        prompt = f"""
Analyze the following user query about global trade and extract the trade parameters:
Identify the trade type (must be either "import" or "export"), the product being traded, and the origin or destination country.

User Query: "{query}"

You must respond with a single, valid JSON object only matching the schema below. Do not include any markdown formatting, backticks, or extra text.

JSON Schema:
{{
  "trade_type": "import" or "export" or "unknown",
  "product": "name of product" or null,
  "country": "name of country" or null
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
            return {
                "trade_type": "unknown",
                "product": None,
                "country": None,
                "error": str(e)
            }
