import os
from pathlib import Path
from typing import List, Dict

def load_documents(knowledge_base_dir: str) -> List[Dict[str, str]]:
    """
    Scans the knowledge_base directory and loads all markdown and text files.
    Returns a list of dictionaries containing the document content and metadata.
    """
    documents = []
    base_path = Path(knowledge_base_dir)
    
    if not base_path.exists() or not base_path.is_dir():
        print(f"Warning: Directory {knowledge_base_dir} does not exist.")
        return documents

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith((".md", ".txt")):
                file_path = Path(root) / file
                
                # Extract category from the parent directory name
                category = file_path.parent.name
                if category == base_path.name:
                    category = "general"
                    
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                documents.append({
                    "content": content,
                    "metadata": {
                        "source": str(file_path),
                        "filename": file,
                        "category": category
                    }
                })
                
    return documents

if __name__ == "__main__":
    # Test the loader
    kb_dir = Path(__file__).parent.parent / "knowledge_base"
    docs = load_documents(str(kb_dir))
    print(f"Loaded {len(docs)} documents.")
    if docs:
        print(f"First document: {docs[0]['metadata']['filename']}")
