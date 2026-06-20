import os
import google.generativeai as genai
from typing import List
from dotenv import load_dotenv

# Ensure we load the environment variables
load_dotenv()

# We configure the API key here or rely on the caller to have configured it
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY and API_KEY != "YOUR_GEMINI_API_KEY":
    genai.configure(api_key=API_KEY)

# Use gemini-embedding-2
EMBEDDING_MODEL = 'models/gemini-embedding-2'

def get_embedding(text: str) -> List[float]:
    """
    Generates a vector embedding for a single text string using Google Gemini.
    """
    try:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        # Return a dummy vector if it fails during testing without an API key
        return [0.0] * 768

def get_query_embedding(text: str) -> List[float]:
    """
    Generates an embedding for a user query.
    Task type 'retrieval_query' is optimized for matching against 'retrieval_document'.
    """
    try:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type="retrieval_query"
        )
        return result['embedding']
    except Exception as e:
        print(f"Error generating query embedding: {e}")
        return [0.0] * 768

def get_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a batch of strings.
    """
    try:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=texts,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"Error generating batch embeddings: {e}")
        return [[0.0] * 768 for _ in texts]
