class RAGService:
    def retrieve(self, query: str) -> list:
        # Mock retrieval from Vector Store
        return [
            {"page_content": "Customs clearance guidelines document states: HS code classification is required.", "metadata": {"source": "customs_guidelines.pdf"}},
            {"page_content": "Import regulations specify import permits must be declared in advance.", "metadata": {"source": "import_regulations.pdf"}},
        ]

rag_service = RAGService()
