# AI-Powered Log Analyzer - Setup Guide

## 🚀 Quick Setup

### 1. Get NVIDIA API Key (Free)

1. Visit [https://build.nvidia.com/](https://build.nvidia.com/)
2. Sign up / Log in with your NVIDIA account
3. Navigate to any model (e.g., "Llama 3.1")
4. Click "Get API Key" or "Python" tab
5. Copy your API key (format: `nvapi-xxxxx`)

### 2. Configure Environment

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your key
NVIDIA_API_KEY=nvapi-your-actual-key-here
```

Or set as environment variable:

**Windows (PowerShell)**:
```powershell
$env:NVIDIA_API_KEY="nvapi-your-actual-key-here"
```

**Linux/Mac**:
```bash
export NVIDIA_API_KEY="nvapi-your-actual-key-here"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `langchain` - Framework for LLM applications
- `langchain-nvidia-ai-endpoints` - NVIDIA AI model integrations
- `langchain-community` - Community tools and integrations
- `faiss-cpu` - Vector similarity search
- `numpy` - Numerical computing
- `python-dotenv` - Environment variable management

### 4. Run the Application

**Option A: Automatic Launcher**
```bash
# Windows
run.bat

# Linux/Mac
bash run.sh
```

**Option B: Manual Start**
```bash
# Terminal 1: Backend
python app.py

# Terminal 2: Frontend
cd frontend
npm install
npm start
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

## 🤖 AI Models Used

### Overview

```
User Upload Log File
        ↓
RecursiveTextSplitter (chunks log into segments)
        ↓
nv-embedqa-e5-v5 (converts text → 768-dim vectors)
        ↓
FAISS Vector Store (indexes embeddings)
        ↓
Semantic Search (retrieves top-4 relevant chunks)
        ↓
Llama 3.1-70B (analyzes chunks + generates insights)
        ↓
Structured Report (root cause + recommendations)
```

### Model Details

| Component | Model/Tool | Purpose | Configuration |
|-----------|------------|---------|---------------|
| **Embeddings** | `nv-embedqa-e5-v5` | Convert text to semantic vectors | 768 dimensions |
| **LLM** | `Llama 3.1-70B-Instruct` | Root cause analysis | Temp=0.1, Max tokens=1024 |
| **Vector DB** | `FAISS` | Similarity search | CPU-optimized |
| **Text Splitter** | `RecursiveCharacterTextSplitter` | Chunk logs | Size=500, Overlap=50 |

## 🔍 How It Works

### 1. Log Processing
```python
# Splits logs into manageable chunks
chunks = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", " "]
).split_text(log_content)
```

### 2. Semantic Embedding
```python
# Converts chunks to 768-dimensional vectors
embeddings = NVIDIAEmbeddings(
    model="nv-embedqa-e5-v5"
).embed_documents(chunks)
```

### 3. Vector Indexing
```python
# Creates FAISS index for fast retrieval
vector_store = FAISS.from_documents(
    chunks, 
    embeddings
)
```

### 4. Semantic Retrieval
```python
# Finds top-4 most relevant chunks for question
relevant_chunks = vector_store.similarity_search(
    question,
    k=4  # Top-4 results
)
```

### 5. LLM Analysis
```python
# Llama 3.1 analyzes retrieved chunks
llm = ChatNVIDIA(
    model="meta/llama-3.1-70b-instruct",
    temperature=0.1  # Factual responses
)
analysis = llm.invoke(prompt_with_context)
```

## 📊 Example Analysis Flow

**Input**: 1000-line authentication log file

**Question**: "Find authentication failures"

**Processing**:
1. ✂️ Split into ~15 chunks (500 chars each)
2. 🧮 Generate 15 × 768-dimensional embeddings
3. 📇 Index in FAISS vector store
4. 🔍 Search: "authentication failures" → Top 4 relevant chunks
5. 🤖 LLM analyzes 4 chunks → Root cause + evidence
6. 📄 Generate structured report

**Output**: 
- Root cause: "Brute force attack detected"
- Evidence: 4 log snippets showing failed attempts
- Severity: Critical
- Actions: ["Block IP", "Enable rate limiting", "Review access logs"]

## 🛡️ Advantages Over Traditional Analysis

| Traditional | AI-Powered (This System) |
|-------------|--------------------------|
| Keyword matching | Semantic understanding |
| Manual pattern recognition | Automatic anomaly detection |
| Static rules | Adaptive reasoning |
| False positives | Context-aware filtering |
| No root cause analysis | Evidence-grounded RCA |

## 🔧 Troubleshooting

### "NVIDIA_API_KEY not found"
- Ensure `.env` file exists in project root
- Check key format: `nvapi-xxxxx`
- Try setting as environment variable

### "AI analysis failed"
- System automatically falls back to rule-based analysis
- Check API key validity at [build.nvidia.com](https://build.nvidia.com/)
- Verify internet connection

### "Module not found: langchain"
- Run: `pip install -r requirements.txt`
- Ensure virtual environment is activated

### "FAISS import error"
- On Windows: Install Visual C++ Redistributable
- Try: `pip install faiss-cpu --upgrade`

## 📚 Additional Resources

- [NVIDIA AI Endpoints Documentation](https://docs.nvidia.com/ai-endpoints/)
- [LangChain Documentation](https://python.langchain.com/)
- [FAISS GitHub](https://github.com/facebookresearch/faiss)
- [Llama 3.1 Model Card](https://huggingface.co/meta-llama/Meta-Llama-3.1-70B-Instruct)

## 🎯 Next Steps

1. Upload a sample log file
2. View AI-powered analysis results
3. Compare with rule-based fallback mode
4. Explore different question types
5. Review evidence chunks backing each finding

---

**Note**: The system gracefully degrades to rule-based analysis if AI models are unavailable, ensuring continuous operation.
