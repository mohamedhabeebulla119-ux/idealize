import re
from typing import List, Dict

def chunk_markdown(content: str, max_chunk_size: int = 1500) -> List[str]:
    """
    Splits a markdown document into smaller chunks.
    It attempts to split by headers (## ) first, then by paragraphs (\n\n).
    """
    # Split by level 2 headings (## ) to keep sections together
    sections = re.split(r'\n(?=## )', content)
    
    chunks = []
    current_chunk = ""
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
            
        # If adding this section exceeds max chunk size and we already have content,
        # save the current chunk and start a new one.
        if len(current_chunk) + len(section) > max_chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = section
        else:
            if current_chunk:
                current_chunk += "\n\n" + section
            else:
                current_chunk = section
                
        # If a single section is larger than max_chunk_size, we need to split it by paragraphs
        if len(current_chunk) > max_chunk_size:
            paragraphs = current_chunk.split("\n\n")
            current_chunk = ""
            for p in paragraphs:
                if len(current_chunk) + len(p) > max_chunk_size and current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = p
                else:
                    if current_chunk:
                        current_chunk += "\n\n" + p
                    else:
                        current_chunk = p
                        
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def process_documents(documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Takes a list of documents and returns a list of chunked documents,
    preserving and extending the metadata with chunk indices.
    """
    chunked_docs = []
    
    for doc in documents:
        content = doc["content"]
        chunks = chunk_markdown(content)
        
        for i, chunk_text in enumerate(chunks):
            # Create a new metadata dict to avoid modifying the original reference
            meta = doc["metadata"].copy()
            meta["chunk_index"] = i
            
            chunked_docs.append({
                "content": chunk_text,
                "metadata": meta
            })
            
    return chunked_docs

if __name__ == "__main__":
    # Simple test
    sample_md = "# Title\n\n## Section 1\n\nContent 1.\n\n## Section 2\n\nContent 2."
    doc = {"content": sample_md, "metadata": {"source": "test.md"}}
    res = process_documents([doc])
    for i, chunk in enumerate(res):
        print(f"--- Chunk {i} ---")
        print(chunk["content"])
