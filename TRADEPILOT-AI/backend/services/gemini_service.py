import google.generativeai as genai
from config import settings

class GeminiService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
        # Using a newer model name that is stable and standard
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_answer(self, prompt: str, context: list) -> str:
        context_text = "\n".join([c.get("page_content", "") for c in context])
        full_prompt = f"Context:\n{context_text}\n\nQuestion: {prompt}"
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error calling Gemini API: {str(e)}"

gemini_service = GeminiService()
