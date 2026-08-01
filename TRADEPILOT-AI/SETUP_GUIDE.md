# TradePilot AI - Full Stack Setup Guide

This guide will help you run the complete TradePilot AI system with the ChatGPT-like frontend connecting to all backend agents and RAG systems.

## Project Structure

```
TRADEPILOT-AI/
├── frontend/           # React + Vite - ChatGPT-like UI
├── backend/            # FastAPI - Multi-agent backend
├── agents/             # AI agents for different functions
├── rag/                # RAG system for knowledge retrieval
├── data/               # Data files and generators
└── knowledge_base/     # Knowledge resources
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- pip (Python package manager)
- npm (Node package manager)

## Installation & Setup

### 1. Backend Setup

#### Create and activate virtual environment:
```bash
cd TRADEPILOT-AI
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

#### Install Python dependencies:
```bash
pip install -r requirements.txt
pip install python-multipart  # Required for file uploads
```

#### Required backend packages:
- fastapi>=0.100.0
- uvicorn>=0.22.0
- pydantic-settings>=2.0.0
- google-generativeai>=0.1.0
- chromadb>=0.4.0
- python-multipart (for file uploads)

### 2. Frontend Setup

#### Navigate to frontend directory:
```bash
cd frontend
```

#### Install Node dependencies:
```bash
npm install
```

#### Create .env.local file:
```
VITE_API_URL=http://localhost:8000/api
```

## Running the Application

### Option A: Run Backend and Frontend Separately (Development)

#### Terminal 1 - Start Backend:
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

Access the API documentation at: http://localhost:8000/docs

#### Terminal 2 - Start Frontend:
```bash
cd frontend
npm run dev
```

You should see:
```
Local: http://localhost:5173/
```

### Option B: Run in Docker (Production)

```bash
# Build and run with docker-compose
docker-compose up -d
```

## Architecture Overview

### Frontend Flow
1. User inputs a query in the ChatGPT-like interface
2. Query is sent to backend
3. Intent Agent analyzes the query
4. Router directs to appropriate agent:
   - **Workflow Agent** - Export/import planning
   - **Compliance Agent** - Regulatory requirements
   - **Risk Agent** - Risk analysis
   - **Checklist Agent** - Readiness checklist
   - **Tariff Agent** - Tariff lookups
   - And more...
5. RAG system retrieves relevant knowledge
6. AI agent generates response using LLM
7. Response is formatted and sent back to frontend
8. Chat history is maintained in context

### Backend Components

#### Multi-Agent System:
- `IntentAgent` - Understands user intent
- `WorkflowAgent` - Creates trade workflows
- `ComplianceAgent` - Checks compliance requirements
- `RiskAgent` - Analyzes risks
- `ChecklistAgent` - Generates checklists
- `TariffAgent` - Searches tariff codes
- And more specialized agents

#### RAG System:
- `Embedder` - Converts documents to embeddings
- `Retriever` - Finds relevant documents
- `VectorStore` - Stores and searches embeddings
- Knowledge Base with:
  - Customs regulations
  - Import/export control rules
  - Tariff schedules
  - Common risks
  - Sample case studies

#### Cache System:
- Caches frequent queries
- Improves response time
- Reduces API calls to LLMs

## API Endpoints

### Chat/Intent
- `POST /api/intent` - Analyze user intent
- Request: `{ "query": "..." }`

### Workflow
- `POST /api/workflow` - Get trade workflow
- Request: `{ "trade_type": "export/import", "product": "...", "country": "..." }`

### Compliance
- `POST /api/compliance` - Check compliance
- Request: `{ "query": "..." }`

### Risk Analysis
- `POST /api/risk` - Analyze risks
- Request: `{ "query": "..." }`

### Checklist
- `POST /api/checklist` - Generate checklist
- Request: `{ "query": "..." }`

### Tariff Search
- `POST /api/tariff-search` - Search tariffs
- Request: `{ "query": "..." }`

### Document Verification
- `POST /api/document-verification` - Verify documents (requires file upload)
- Form data with file and verification parameters

### Health Check
- `GET /api/health` - Check backend status

## Frontend Features

### Chat Interface
- ✅ ChatGPT-like conversation UI
- ✅ Conversation history management
- ✅ Multi-turn conversations with context
- ✅ Intent detection display
- ✅ Formatted responses for different agents
- ✅ Mobile responsive design
- ✅ Real-time typing indicators
- ✅ Error handling

### Sidebar Navigation
- Create new conversations
- View conversation history
- Delete conversations
- Quick access to example prompts

### Example Prompts
- "What are the export requirements for tea to the UK?"
- "What are the risks of importing motorcycles?"
- "Give me a compliance checklist for cinnamon export"
- "What are the tariff codes for electronics?"

## Troubleshooting

### Issue: "python-multipart" not installed
**Solution:**
```bash
pip install python-multipart
```

### Issue: CORS errors from frontend
**Solution:** The backend is configured with CORS. Ensure frontend is making requests to `http://localhost:8000/api`

### Issue: Port 8000 already in use
**Solution:** Use different port
```bash
python -m uvicorn main:app --reload --port 8001
```

### Issue: Frontend can't connect to backend
**Solution:** Check `.env.local` has correct API URL:
```
VITE_API_URL=http://localhost:8000/api
```

### Issue: RAG system not returning results
**Solution:** Ensure ChromaDB vector database is initialized:
```bash
python data/bulk_synthetic_data_generator.py
```

## Development Workflow

1. **Frontend Development:**
   - Edit React components in `frontend/src/`
   - Hot reload via Vite
   - Check `http://localhost:5173/`

2. **Backend Development:**
   - Edit agents in `backend/agents/`
   - Hot reload via `--reload` flag
   - Check `http://localhost:8000/docs` for API testing

3. **Adding New Agents:**
   - Create new agent class in `agents/`
   - Create route in `backend/routes/`
   - Register router in `backend/main.py`
   - Add handler to chat service

4. **Knowledge Base Updates:**
   - Add documents to `knowledge_base/`
   - Update RAG loader if needed
   - Regenerate embeddings

## Performance Optimization

1. **Caching:** Backend caches frequent queries
2. **Vector Database:** ChromaDB stores embeddings locally
3. **Connection Pooling:** FastAPI manages database connections
4. **Frontend:** Code splitting and lazy loading via Vite

## Security Notes

⚠️ **Development Only:** Current setup has:
- CORS: Allow all origins
- No authentication
- No rate limiting

For production:
1. Enable proper CORS configuration
2. Add authentication (JWT, OAuth, etc.)
3. Add rate limiting
4. Use environment variables for secrets
5. Enable HTTPS
6. Add input validation
7. Implement logging and monitoring

## Next Steps

1. ✅ Start backend
2. ✅ Start frontend
3. ✅ Open http://localhost:5173
4. ✅ Chat with TradePilot AI!
5. Test different agent capabilities
6. Customize response formatting
7. Add more knowledge base documents
8. Deploy to production

## Support

For issues or questions:
1. Check API docs: http://localhost:8000/docs
2. Check browser console for frontend errors
3. Check terminal output for backend logs
4. Review error messages in chat interface

---

**Happy Trading! 🚀**
