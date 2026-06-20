from typing import List, Dict, Any
from rag.embedding import get_query_embedding
from rag.vector_store import query_vector_store

def retrieve_context(query: str, n_results: int = 5) -> str:
    """
    Retrieves the most relevant context for a given query from the vector store.
    Returns a formatted string containing the context passages and their sources.
    """
    # 1. Embed the query
    query_emb = get_query_embedding(query)
    
    # 2. Query the vector store
    results = query_vector_store(query_emb, n_results=n_results)
    
    # 3. Format the results
    if not results or not results.get("documents") or len(results["documents"][0]) == 0:
        return "No relevant regulatory context found in the knowledge base."
        
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    
    formatted_contexts = []
    
    for i, (doc, meta) in enumerate(zip(documents, metadatas)):
        source = meta.get("filename", "Unknown Source")
        category = meta.get("category", "General")
        
        context_block = f"--- Source {i+1}: {source} (Category: {category}) ---\n{doc}\n"
        formatted_contexts.append(context_block)
        
    return "\n".join(formatted_contexts)

def build_index(knowledge_base_dir: str):
    """
    Helper function to load, chunk, embed, and store the entire knowledge base.
    """
    from rag.loader import load_documents
    from rag.chunker import process_documents
    from rag.embedding import get_embeddings_batch
    from rag.vector_store import add_to_vector_store, reset_vector_store
    
    print("Loading documents...")
    docs = load_documents(knowledge_base_dir)
    print(f"Loaded {len(docs)} documents.")
    
    if not docs:
        print("No documents found to index.")
        return
        
    print("Chunking documents...")
    chunked_docs = process_documents(docs)
    print(f"Created {len(chunked_docs)} chunks.")
    
    print("Generating embeddings...")
    texts = [doc["content"] for doc in chunked_docs]
    # In a real app with many chunks, we should batch this to avoid API limits
    embeddings = get_embeddings_batch(texts)
    
    print("Storing in vector database...")
    # Optional: reset before building to avoid duplicates during testing
    # reset_vector_store() 
    add_to_vector_store(chunked_docs, embeddings)
    print("Indexing complete.")

if __name__ == "__main__":
    # Test retrieval
    test_query = "What are the rules for exporting cinnamon?"
    print(f"Retrieving for: '{test_query}'")
    context = retrieve_context(test_query)
    print(context)
