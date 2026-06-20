import os
import json
import time
from typing import Dict, Any, List
from google import genai
from google.genai import types
from dotenv import load_dotenv

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.retriever import retrieve_context

# Load .env file from project root
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

class IntentAgent:
    """
    Master Query Router implementing Advanced RAG.
    Performs Intelligent Routing, Query Decomposition, Synthesis, and Self-Evaluation.
    """
    def __init__(self) -> None:
        self.name = "Advanced RAG Query Engine"
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        if api_key:
            self.client = genai.Client(api_key=api_key)
        # We define a standard delay to respect rate limits between pipeline steps
        self.delay = 3

    def _safe_generate(self, prompt: str, require_json: bool = True) -> str:
        """Helper to run genai generation with rate limit protection."""
        if not self.client:
            raise Exception("API Client not configured.")
            
        config = types.GenerateContentConfig()
        if require_json:
            config.response_mime_type = "application/json"
            
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config
        )
        
        text = response.text.strip()
        if require_json and text.startswith("```"):
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:-1]
            text = "\n".join(lines).strip()
            
        return text

    def _route_query(self, query: str) -> Dict[str, Any]:
        """Step 1: Intelligent Routing"""
        prompt = f"""
Analyze the following user query. Determine if it is a 'greeting' (casual chat, hello, thanks) or a 'trade_query' (asking about imports, exports, customs, taxes, workflow).
If it is a greeting, generate a polite reply. If it is a trade_query, reply field can be empty.

User Query: "{query}"

JSON Schema:
{{
  "type": "greeting" or "trade_query",
  "reply": "Polite response if greeting, else empty string"
}}
"""
        res = self._safe_generate(prompt)
        return json.loads(res)

    def _synthesize_answers(self, query: str) -> str:
        """Step 2: Synthesis via RAG"""
        # Retrieve context for the main query
        ctx = retrieve_context(query, n_results=5)
        
        prompt = f"""
You are TradePilot AI. Use the following extracted knowledge base context to answer the user's query.
Synthesize the information into a single cohesive, professional, and comprehensive response.

--- Knowledge Base Context ---
{ctx}
------------------------------

User Query: "{query}"

Draft a comprehensive answer based ONLY on the provided context.
"""
        # Sleep before synthesis LLM call
        time.sleep(self.delay)
        return self._safe_generate(prompt, require_json=False)

    def _evaluate_response(self, original_query: str, draft_response: str) -> Dict[str, Any]:
        """Step 4: Self Evaluation (Grader)"""
        prompt = f"""
You are a strict Evaluator. Review the Draft Response to see if it accurately and fully answers the Original User Query.
If the Draft Response indicates that the context does not have the information, mark it as relevant=false.

Original User Query: "{original_query}"
Draft Response: "{draft_response}"

If relevant=true, return the draft response as improved_response. 
If relevant=false, provide a polite improved_response apologizing that the information is missing from the knowledge base.

JSON Schema:
{{
  "relevant": true or false,
  "reason": "Why it passed or failed",
  "improved_response": "The final response to show the user"
}}
"""
        # Sleep before evaluation LLM call
        time.sleep(self.delay)
        res = self._safe_generate(prompt)
        return json.loads(res)

    def process(self, query: str) -> Dict[str, Any]:
        """Main Pipeline Execution"""
        try:
            # 1. Route
            route_data = self._route_query(query)
            if route_data.get("type") == "greeting":
                return {
                    "query": query,
                    "type": "greeting",
                    "final_response": route_data.get("reply", "Hello! How can I assist you with trade compliance today?"),
                    "pipeline_steps": ["Routing completed"]
                }
            
            time.sleep(self.delay)
            
            # 2. Synthesize
            draft = self._synthesize_answers(query)
            
            # 3. Evaluate
            evaluation = self._evaluate_response(query, draft)
            
            return {
                "query": query,
                "type": "trade_query",
                "draft_response": draft,
                "evaluation": evaluation,
                "final_response": evaluation.get("improved_response", draft),
                "pipeline_steps": ["Routed", "Synthesized", "Evaluated"]
            }
        except Exception as e:
            return {
                "query": query,
                "type": "error",
                "final_response": f"An error occurred during query processing: {str(e)}",
                "pipeline_steps": ["Failed"]
            }
