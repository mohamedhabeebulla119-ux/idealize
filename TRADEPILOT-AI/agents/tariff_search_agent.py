import os
import json
from typing import Dict, Any
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load .env file from project root (parent directory of agents/)
dotenv_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

class TariffSearchAgent:
    """
    TariffSearchAgent performs real-time Google Search grounding to retrieve
    the latest customs tariff rates (Duty, VAT, PAL) in Sri Lanka for a product or HS Code.
    """
    def __init__(self) -> None:
        api_key: str | None = os.getenv("GEMINI_API_KEY")
        self.client: genai.Client | None = None
        if api_key:
            self.client = genai.Client(api_key=api_key)

    def search_tariff_rates(self, product: str, hs_code: str) -> Dict[str, Any]:
        """
        Searches the web for latest tax rates for a given HS code or product.
        Returns a dictionary containing duty, vat, pal, and source info.
        """
        if not self.client:
            print("[TariffSearchAgent] API Client not configured. Using fallback rates.")
            return {
                "duty": 10.0,
                "vat": 18.0,
                "pal": 5.0,
                "source": "fallback (no client)"
            }

        prompt = f"""
Search the web to find the latest Sri Lanka Customs import tariff rates (Duty, VAT, PAL) for the product '{product}' (HS Code: '{hs_code}').
Look for official Sri Lanka Customs tariff guides or reliable trade portals (like tariff.lk or customs.gov.lk).

You must respond with a single, valid JSON object only matching the schema below. Do not include any markdown formatting, backticks, or extra text.

JSON Schema:
{{
  "duty": float (percentage, e.g. 15.0 or 0.0),
  "vat": float (percentage, e.g. 18.0),
  "pal": float (percentage, e.g. 10.0 or 5.0),
  "source_url": "string (the URL where you found this information)"
}}

If you cannot find specific rates, return fallback values:
{{
  "duty": 10.0,
  "vat": 18.0,
  "pal": 5.0,
  "source_url": "fallback"
}}
"""
        try:
            print(f"[TariffSearchAgent] Grounding web search for Product: {product}, HS Code: {hs_code}...")
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=[types.Tool(google_search=types.GoogleSearch())],
                    response_mime_type="application/json"
                )
            )
            
            text = response.text.strip()
            # Clean possible markdown wrap if the model ignored response_mime_type instructions
            if text.startswith("```"):
                lines = text.split("\n")
                if lines[0].startswith("```json") or lines[0].startswith("```"):
                    lines = lines[1:-1]
                text = "\n".join(lines).strip()
                
            data = json.loads(text)
            
            # Ensure return rates are parsed correctly as floats
            rates = {
                "duty": float(data.get("duty", 10.0)),
                "vat": float(data.get("vat", 18.0)),
                "pal": float(data.get("pal", 5.0)),
                "source": data.get("source_url", "web_search")
            }
            print(f"[TariffSearchAgent] Successfully fetched from web search: {rates}")
            return rates
            
        except Exception as e:
            # Fall back to standard estimates if we hit rate limits (429) or other API exceptions
            print(f"[TariffSearchAgent] Search failed or quota exceeded: {str(e)}. Using fallback rates.")
            return {
                "duty": 10.0,
                "vat": 18.0,
                "pal": 5.0,
                "source": f"fallback (due to search error or API quota limit)"
            }
