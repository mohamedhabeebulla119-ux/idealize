# TradePilot AI

**TradePilot AI** is an AI-powered intelligent trade assistance platform designed to guide users throughout the entire import and export lifecycle in Sri Lanka. The platform transforms complex regulatory procedures into personalized, easy-to-follow workflows, bridging the gap between government regulations and practical business execution.

Now featuring a **ChatGPT-like conversational interface** that connects to multiple specialized agents for compliance, risk analysis, workflow planning, and more!

## Vision
To automate and streamline global trade compliance, reducing customs clearance issues and ensuring full alignment with international trade law.

## ✨ Features
* **ChatGPT-like Chat Interface:** Conversational UI for easy interaction with trade compliance system
* **Intelligent Process Navigation:** Generates tailored, step-by-step import and export roadmaps
* **Automated Compliance Guidance:** Identifies required permits, approvals, certifications, and documentation
* **Risk Assessment:** Detects missing compliance obligations and potential validation errors
* **Cost and Timeline Awareness:** Projects estimated financial overheads and procedural durations
* **Retrieval-Augmented Generation (RAG):** Powered by an authoritative regulatory knowledge base
* **Multi-Agent System:** Specialized agents for workflows, compliance, risks, checklists, tariffs, and more

## 🚀 Quick Start

### 1. One-Command Startup (Recommended)

#### Windows:
```bash
start-all.bat
```

#### Mac/Linux:
```bash
chmod +x start-all.sh
./start-all.sh
```

### 2. Manual Setup

#### Install dependencies:
```bash
# Backend
pip install -r requirements.txt
pip install python-multipart

# Frontend
cd frontend
npm install
```

#### Terminal 1 - Start Backend:
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

#### Terminal 2 - Start Frontend:
```bash
cd frontend
npm run dev
```

### 3. Access the Application
- 🎯 **Frontend Chat:** http://localhost:5173
- 📚 **API Documentation:** http://localhost:8000/docs
- 🏥 **Health Check:** http://localhost:8000/health

## 💬 How to Use

### Example 1: Export Planning
```
You: "What are the export requirements for tea to the UK?"

TradePilot AI: [Shows export workflow, requirements, risks, and costs]
```

### Example 2: Risk Analysis
```
You: "I want to import motorcycles from Japan. What are the risks?"

TradePilot AI: [Analyzes and lists potential risks with mitigation strategies]
```

### Example 3: Compliance Checklist
```
You: "Give me a compliance checklist for cinnamon export"

TradePilot AI: [Generates organized checklist with all requirements]
```

## 📋 Prerequisites
* Python 3.8+
* Node.js 16+
* Google Gemini API Key (for AI features)
* pip and npm package managers

## 🏗️ Architecture

```
Frontend (React + Vite)
    ↓
Chat Service (Intent + Routing)
    ↓
Intent Agent (Detects user intent)
    ↓
Specialized Agents:
├── Workflow Agent (Planning)
├── Compliance Agent (Regulations)
├── Risk Agent (Risk Analysis)
├── Checklist Agent (Readiness)
├── Tariff Agent (HS Codes)
├── Document Agent (Verification)
└── Cost Agent (Estimation)
    ↓
RAG System (Knowledge Retrieval)
    ↓
LLM (Google Gemini)
    ↓
Response to User
```

## 📁 Project Structure
```
TRADEPILOT-AI/
├── frontend/              # React + Vite ChatGPT-like UI
│   ├── src/
│   │   ├── pages/
│   │   │   └── Chat.jsx        # Main chat interface
│   │   ├── components/
│   │   ├── context/
│   │   │   └── ChatContext.jsx # State management
│   │   ├── services/
│   │   │   └── chatService.js  # API communication
│   │   └── styles/
│   │       └── Chat.css        # Modern styling
│   └── package.json
│
├── backend/               # FastAPI backend
│   ├── main.py           # Application entry point
│   ├── config.py         # Configuration
│   ├── routes/           # API endpoints
│   │   ├── intent.py
│   │   ├── workflow.py
│   │   ├── compliance.py
│   │   ├── risk.py
│   │   ├── checklist.py
│   │   └── ... more routes
│   ├── models/           # Pydantic models
│   └── services/         # Business logic
│
├── agents/               # Multi-agent system
│   ├── intent_agent.py
│   ├── workflow_agent.py
│   ├── compliance_agent.py
│   ├── risk_agent.py
│   └── ... more agents
│
├── rag/                  # RAG implementation
│   ├── loader.py         # Document loading
│   ├── chunker.py        # Text chunking
│   ├── embedding.py      # Embeddings
│   ├── vector_store.py   # Vector storage
│   └── retriever.py      # Document retrieval
│
├── knowledge_base/       # Knowledge resources
│   ├── customs/
│   ├── government/
│   ├── import_export_control/
│   └── sample_cases/
│
├── data/                 # Data generation
│   ├── synthetic_data_generator.py
│   └── bulk_synthetic_data_generator.py
│
└── requirements.txt      # Python dependencies
```

## 🔧 Configuration

### Environment Variables
Create `.env` or use `.env.local` in frontend:
```env
VITE_API_URL=http://localhost:8000/api
GEMINI_API_KEY=your_api_key_here
```

### Backend Configuration
Edit `backend/config.py` for:
- LLM settings
- RAG parameters
- Cache configuration
- Database paths

## 📖 Documentation
- [Setup Guide](./SETUP_GUIDE.md) - Detailed installation and configuration
- [Chat Guide](./CHAT_GUIDE.md) - How to use the chat interface
- [Technical Architecture](./docs/technical_architecture.md) - System design details
- [Project Overview](./PROJECT_OVERVIEW.md) - Full project documentation

## 🧪 Testing

### Test RAG Pipeline:
```bash
python tests/test_rag_engine.py
```

### Test API Routes:
```bash
pytest tests/test_api_routes.py -v
```

### Test Cache:
```bash
pytest tests/test_cache.py -v
```

## 📊 API Endpoints

### Chat & Intent
- `POST /api/intent` - Analyze user intent
- Request: `{ "query": "..." }`

### Workflows
- `POST /api/workflow` - Get trade workflow
- Request: `{ "trade_type": "export/import", "product": "...", "country": "..." }`

### Compliance
- `POST /api/compliance` - Check compliance requirements
- Request: `{ "query": "..." }`

### Risk Analysis
- `POST /api/risk` - Analyze potential risks
- Request: `{ "query": "..." }`

### Checklists
- `POST /api/checklist` - Generate checklist
- Request: `{ "query": "..." }`

### Tariff Search
- `POST /api/tariff-search` - Search tariff codes
- Request: `{ "query": "..." }`

See [API Documentation](http://localhost:8000/docs) for complete details.

## 🛠️ Technology Stack

### Frontend
- React 18
- Vite (build tool)
- React Router (navigation)
- Lucide React (icons)
- Modern CSS

### Backend
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Pydantic (data validation)
- Python-multipart (file uploads)

### AI & ML
- Google Gemini (LLM)
- ChromaDB (vector database)
- Embedding models (text-embedding-004)

### Data & Storage
- JSON (configuration)
- SQLite (optional)
- ChromaDB (vector storage)

## 🚨 Getting Help

### Issue: "python-multipart" not installed
```bash
pip install python-multipart
```

### Issue: CORS errors
Ensure backend is running and `.env.local` has correct API URL

### Issue: Port already in use
```bash
# Change port in backend
python -m uvicorn main:app --reload --port 8001
```

### Check Logs
- Backend: Check terminal running `uvicorn` command
- Frontend: Check browser console (F12)
- API Docs: http://localhost:8000/docs

## 📝 Environment Setup (.env)

```env
# Backend Configuration
GEMINI_API_KEY=your_api_key_here
VECTOR_DB_PATH=./vector_db/chroma_db

# Frontend Configuration
VITE_API_URL=http://localhost:8000/api

# Optional
DEBUG=true
LOG_LEVEL=INFO
CACHE_ENABLED=true
```

## 🎯 Next Steps
1. ✅ Install dependencies
2. ✅ Start backend and frontend
3. ✅ Open http://localhost:5173
4. ✅ Chat with TradePilot AI!
5. 📖 Read [Chat Guide](./CHAT_GUIDE.md) for tips
6. 🔌 Integrate additional agents as needed
7. 🚀 Deploy to production

## 📄 License
[Your License Here]

## 👥 Contributing
Contributions are welcome! Please refer to [Contributing Guidelines](./CONTRIBUTING.md).

## 🤝 Support
For issues, questions, or suggestions:
1. Check existing documentation
2. Review API docs at http://localhost:8000/docs
3. Check browser console for frontend errors
4. Review backend terminal logs

---

**TradePilot AI - Simplifying Global Trade Compliance** 🌍✈️📦
- `knowledge_base/`: Markdown documents representing authoritative trade regulations used for grounding AI responses.
- `rag/`: The RAG pipeline modules (`loader.py`, `chunker.py`, `embedding.py`, `vector_store.py`, `retriever.py`, `prompt_templates.py`).
- `frontend/`: Frontend application code.
