import os
# pyrefly: ignore [missing-import]
import chromadb
from typing import List, Dict, Any
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()

# We store the Chroma database in the directory specified by .env or a default
DB_DIR = os.getenv("CHROMA_DB_DIR", "vector_db/chroma_db")
COLLECTION_NAME = "trade_regulations"

def get_chroma_client():
    """Initializes and returns a ChromaDB client."""
    # Ensure the directory exists
    os.makedirs(DB_DIR, exist_ok=True)
    client = chromadb.PersistentClient(path=DB_DIR)
    return client

def get_or_create_collection(client):
    """Retrieves the collection or creates it if it doesn't exist."""
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"} # Cosine similarity is typically best for text embeddings
    )

def add_to_vector_store(chunked_docs: List[Dict[str, Any]], embeddings: List[List[float]]):
    """
    Adds chunked documents and their embeddings to the ChromaDB collection.
    """
    if not chunked_docs or not embeddings:
        return
        
    client = get_chroma_client()
    collection = get_or_create_collection(client)
    
    ids = []
    documents = []
    metadatas = []
    
    for i, doc in enumerate(chunked_docs):
        # Create a unique ID for each chunk based on its source and index
        source = doc["metadata"].get("source", "unknown")
        chunk_idx = doc["metadata"].get("chunk_index", 0)
        
        # Clean up path separators for ID
        clean_source = os.path.basename(source)
        doc_id = f"{clean_source}_chunk_{chunk_idx}_{i}"
        
        ids.append(doc_id)
        documents.append(doc["content"])
        
        # Ensure all metadata values are primitive types (str, int, float, bool)
        clean_meta = {k: str(v) if not isinstance(v, (str, int, float, bool)) else v 
                     for k, v in doc["metadata"].items()}
        metadatas.append(clean_meta)
        
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
    
    print(f"Successfully added {len(ids)} chunks to the vector store.")

def query_vector_store(query_embedding: List[float], n_results: int = 5) -> Dict[str, Any]:
    """
    Queries the vector store using an embedding and returns the top n_results.
    """
    client = get_chroma_client()
    collection = get_or_create_collection(client)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results

def reset_vector_store():
    """Deletes the collection (useful for rebuilding the index)."""
    client = get_chroma_client()
    try:
        client.delete_collection(COLLECTION_NAME)
        print("Collection deleted.")
    except Exception as e:
        print(f"Error deleting collection: {e}")
