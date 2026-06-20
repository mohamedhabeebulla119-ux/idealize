def test_rag_retrieval():
    from backend.services.rag_service import rag_service
    results = rag_service.retrieve("HS code for motorcycle")
    assert len(results) > 0
    assert "HS code" in results[0]["page_content"]
