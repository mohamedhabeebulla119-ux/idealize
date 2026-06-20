import os
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

from rag.retriever import build_index, retrieve_context
from rag.prompt_templates import build_rag_prompt

def test_rag_pipeline():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    has_valid_key = api_key and api_key != "YOUR_GEMINI_API_KEY"
    
    if has_valid_key:
        genai.configure(api_key=api_key)
    else:
        print("WARNING: Valid GEMINI_API_KEY not found. Embeddings will be mocked, and LLM generation will be skipped.")

    # 1. Build Index
    print("\n--- Step 1: Building Vector Index ---")
    kb_dir = str(Path(__file__).parent / "knowledge_base")
    build_index(kb_dir)
    
    # 2. Test Query Retrieval
    print("\n--- Step 2: Retrieving Context ---")
    queries = [
        "What are the taxes for importing electronics?",
        "Do I need a phytosanitary certificate to export cinnamon to Dubai?"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        context = retrieve_context(query, n_results=2)
        print("Retrieved Context Snippet:")
        print(context[:500] + "...\n")
        
        # 3. Generate Prompt
        print("--- Step 3: Generating RAG Prompt ---")
        prompt = build_rag_prompt(query, context)
        
        # 4. LLM Response
        if has_valid_key:
            print("--- Step 4: Generating LLM Response ---")
            try:
                model = genai.GenerativeModel('models/gemini-2.5-flash')
                response = model.generate_content(prompt)
                print(f"Response:\n{response.text}\n")
            except Exception as e:
                print(f"LLM Generation failed: {e}")
        else:
            print("Skipping LLM response (no valid API key).")
            print("Prompt that would be sent to LLM:")
            print("-" * 40)
            print(prompt[:500] + "...")
            print("-" * 40)

if __name__ == "__main__":
    test_rag_pipeline()
