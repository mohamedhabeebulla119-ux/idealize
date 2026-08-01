import os
import sys
import json
from typing import Dict, List, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Ensure parent directory is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.chunker import chunk_markdown
from rag.embedding import get_embeddings_batch, get_query_embedding
from rag.vector_store import add_to_vector_store, query_vector_store
from rag.retriever import retrieve_context

load_dotenv()

class ChatAgent:
    """
    ChatAgent acts like a ChatGPT assistant with custom document context.
    It can ingest custom user files (PDFs/Text) and perform conversational QA.
    """
    def __init__(self) -> None:
        api_key: str | None = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def ingest_custom_document(self, filename: str, content: str) -> Dict[str, Any]:
        """
        Chunks the document content, generates embeddings, and adds it to the Chroma vector store.
        """
        try:
            if not content.strip():
                return {"status": "error", "message": "Document content is empty."}

            # 1. Chunk document
            chunks = chunk_markdown(content)
            
            # 2. Build chunk dictionaries with metadata
            chunked_docs = []
            for i, chunk_text in enumerate(chunks):
                chunked_docs.append({
                    "content": chunk_text,
                    "metadata": {
                        "source": filename,
                        "filename": filename,
                        "category": "user_upload",
                        "chunk_index": i
                    }
                })

            # 3. Embed chunks
            texts = [doc["content"] for doc in chunked_docs]
            embeddings = get_embeddings_batch(texts)

            # 4. Add to Chroma
            add_to_vector_store(chunked_docs, embeddings)

            return {
                "status": "success",
                "message": f"Successfully ingested {filename} with {len(chunks)} chunks."
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def chat(self, user_message: str, history: List[Dict[str, str]] = []) -> Dict[str, Any]:
        """
        Performs retrieval from Chroma vector store and generates a response using conversational context.
        """
        try:
            # 1. Retrieve relevant context for the query
            context = retrieve_context(user_message, n_results=5)
            
            # 2. Build conversational prompt
            history_str = ""
            for turn in history:
                role = "User" if turn.get("role") == "user" else "Assistant"
                history_str += f"{role}: {turn.get('content')}\n"

            prompt = f"""
You are TradePilot AI, a knowledgeable assistant specializing in Sri Lanka trade compliance and customs regulations.
Help the user answer their query based on the conversational history and regulatory context below.

--- Regulatory Context ---
{context}
--------------------------

--- Conversation History ---
{history_str}
----------------------------

User Query: {user_message}

CRITICAL RULES:
1. Provide a professional, clear, and structured response.
2. Rely strictly on the facts provided in the Regulatory Context.
3. If the context does not contain relevant information, politely inform the user, but still try to offer general helpful guidance if possible.
4. Keep the tone helpful and friendly (like ChatGPT).
"""
            # 3. Call Gemini
            response = self.model.generate_content(prompt)
            
            return {
                "response": response.text.strip(),
                "retrieved_context": context
            }
        except Exception as e:
            return {
                "response": f"Sorry, I encountered an error: {str(e)}",
                "retrieved_context": ""
            }
