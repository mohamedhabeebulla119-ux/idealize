import os
from rag.retriever import retrieve_context

def test_rag_retrieval_returns_string():
    # ChromaDB retrieve_context should gracefully return a string
    # even if it fails or succeeds.
    query = "Test query for medical devices"
    result = retrieve_context(query, n_results=1)
    
    assert isinstance(result, str)
    # It should either return context from the DB or a fallback message
    assert len(result) > 0
