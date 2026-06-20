# TradePilot AI

**TradePilot AI** is an AI-powered intelligent trade assistance platform designed to guide users throughout the entire import and export lifecycle in Sri Lanka. The platform transforms complex regulatory procedures into personalized, easy-to-follow workflows, bridging the gap between government regulations and practical business execution.

## Vision
To automate and streamline global trade compliance, reducing customs clearance issues and ensuring full alignment with international trade law.

## Features
* **Intelligent Process Navigation:** Generates tailored, step-by-step import and export roadmaps.
* **Automated Compliance Guidance:** Identifies required permits, approvals, certifications, and documentation.
* **Risk Assessment:** Detects missing compliance obligations and potential validation errors.
* **Cost and Timeline Awareness:** Projects estimated financial overheads and procedural durations.
* **Retrieval-Augmented Generation (RAG):** Powered by an authoritative regulatory knowledge base to ensure accurate and grounded responses.

## Getting Started

### Prerequisites
* Python 3.9+
* Google Gemini API Key

### Installation
1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Update the `.env` file with your `GEMINI_API_KEY`:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### Running the RAG Pipeline Test
To verify that the RAG pipeline is correctly building the vector index, embedding the knowledge base, and generating answers with the Gemini LLM, run the test script:

```bash
python test_rag.py
```

This script will:
1. Load synthetic regulatory markdown documents from `knowledge_base/`.
2. Chunk them and embed them using `models/text-embedding-004`.
3. Store the embeddings locally in a ChromaDB database (`vector_db/chroma_db`).
4. Perform sample queries and pass the retrieved context to Gemini to answer trade compliance questions.

## Project Structure
- `agents/`: Contains the specialized multi-agent architecture.
- `backend/`: FastAPI application backend (To be implemented).
- `data/`: Data generation scripts (e.g., `synthetic_data_generator.py`).
- `docs/`: System requirements and problem statement documentation.
- `knowledge_base/`: Markdown documents representing authoritative trade regulations used for grounding AI responses.
- `rag/`: The RAG pipeline modules (`loader.py`, `chunker.py`, `embedding.py`, `vector_store.py`, `retriever.py`, `prompt_templates.py`).
- `frontend/`: Frontend application code.
