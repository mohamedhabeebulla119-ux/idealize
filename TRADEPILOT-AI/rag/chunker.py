class TextChunker:
    def chunk(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
        # Mock chunking
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size - chunk_overlap)]
