# Anomaly Report Analyzer

AI-powered log analysis and anomaly detection system using NVIDIA AI models, FAISS vector search, and LangChain.

## 🤖 AI Models & Technology Stack

This project leverages state-of-the-art AI models for intelligent log analysis:

### 1. **Semantic Embedding Model**
- **Model**: `nv-embedqa-e5-v5` (NVIDIA AI Endpoints)
- **Purpose**: Convert unstructured log text into 768-dimensional semantic vectors
- **Function**: Enables semantic understanding beyond keyword matching - finds related errors even with different wording

### 2. **Large Language Model (LLM)**
- **Model**: `Llama 3.1-70B-Instruct` (via ChatNVIDIA)
- **Purpose**: Core reasoning engine for anomaly detection and root cause analysis
- **Configuration**: 
  - Temperature: 0.1 (low temperature for factual, evidence-backed responses)
  - Max tokens: 1024
- **Function**: Processes retrieved log chunks to diagnose issues, preventing hallucination by grounding answers in actual data

### 3. **Vector Retrieval System**
- **Tool**: `FAISS` (Facebook AI Similarity Search)
- **Purpose**: Index vector embeddings for ultra-fast similarity search
- **Function**: O(1) similarity search to instantly retrieve top-4 most relevant log chunks from thousands of entries

### 4. **Text Processing**
- **Tool**: `RecursiveCharacterTextSplitter` (LangChain)
- **Purpose**: Intelligent text chunking with hierarchical separators
- **Function**: 
  - Chunk size: 500 characters (keeps 1-3 related log entries together)
  - Overlap: 50 characters (preserves context across boundaries)
  - Hierarchical separators: `\n\n`, `\n`, ` ` (maintains log structure)

## Features

- **AI-Powered Analysis**: Semantic search + LLM reasoning for accurate root cause detection
- **File Upload Analysis**: Upload log files (.log, .txt) for AI analysis
- **Text Analysis**: Paste log content directly for instant AI-powered insights
- **Multi-Question Analysis**: 5 different security perspectives per log
  - Anomaly Detection
  - Authentication Failure Detection
  - Brute Force Attack Detection
  - User Session Anomalies
  - Resource & Configuration Anomalies
- **Evidence-Grounded Reports**: Every finding backed by actual log entries (no hallucination)
- **Real-time Metrics**: Performance monitoring and API metrics
- **Professional UI**: Clean, modern Bootstrap interface
- **Fallback Support**: Gracefully falls back to rule-based analysis if AI unavailable

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+
- Git
- **NVIDIA API Key** (Get free key at [build.nvidia.com](https://build.nvidia.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository>
   cd AnomalyReportProject
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your NVIDIA_API_KEY
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the launcher**
   - Windows: `run.bat`
   - Linux/Mac: `bash run.sh`

   Or manually:

5. **Backend Setup**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   
   pip install -r requirements.txt
   python app.py
   ```

4. **Frontend Setup** (new terminal)
   ```bash
   cd frontend
   npm install
   npm start
   ```

## Access

- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:5000

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/analyze` - Upload and analyze file
- `POST /api/analyze-text` - Analyze text content
- `GET /api/metrics` - Performance metrics

## Project Structure

```
├── app.py                    # Flask main application
├── requirements.txt          # Python dependencies
├── run.bat                  # Windows launcher
├── run.sh                   # Linux/Mac launcher
├── backend/
│   ├── models/              # Data models
│   │   └── metrics.py
│   ├── services/            # Business logic
│   │   ├── analyzer.py      # Log analysis
│   │   └── generator.py     # Report generation
│   ├── routes/              # API routes
│   │   ├── health.py
│   │   └── analysis.py
│   └── utils/               # Utilities
│       └── file_utils.py
├── frontend/                # React application
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   │   ├── FileUploadForm.js
│   │   │   ├── ReportDisplay.js
│   │   │   └── LoadingSpinner.js
│   │   └── styles/
│   └── package.json
├── sample_logs/             # Example log files
├── uploads/                 # Temporary upload storage
├── docker-compose.yml       # Docker Compose config
├── Dockerfile.backend       # Backend image
├── Dockerfile.frontend      # Frontend image
└── k8s-deployment.yaml      # Kubernetes manifests

```

## Technologies

- **Backend**: Flask 2.3.0, Python 3.10+, Gunicorn
- **Frontend**: React 18.2, CSS3
- **Deployment**: Docker, Docker Compose, Kubernetes
- **Analysis**: Content-aware log processing with 10+ metrics

## Key Features of Analysis

### Log Content Processing
- Extracts 10 different metrics from log content
- Real-time statistics calculation
- Context-aware severity assessment

### Question-Specific Reports
Each question generates completely unique reports:
1. **Analyze anomaly in logs** - Comprehensive error analysis
2. **Find authentication failure** - Auth security assessment
3. **Detect brute force attack patterns** - SSH attack detection
4. **Check abnormal user sessions** - Session anomalies
5. **Find resource and configuration anomalies** - System health

### Confidence Scoring
- Dynamic confidence calculation based on file content
- Question-specific thresholds
- Evidence-based severity assessment

## Deployment

### Docker
```bash
docker-compose up --build
```

### Kubernetes
```bash
kubectl apply -f k8s-deployment.yaml
```

### Azure Deployment
See DEPLOYMENT.md for detailed instructions

## Development

### Running Tests
```bash
pytest tests/
```

### Backend Development
```bash
python app.py  # With Flask debug mode
```

### Frontend Development
```bash
cd frontend
npm start  # With hot reload
```

## Documentation

- `ARCHITECTURE.md` - System design and components
- `DEPLOYMENT.md` - Cloud deployment guide
- `CONTAINERIZATION.md` - Docker/Kubernetes setup
- `QUICK_START.md` - Quick reference guide

## License

Proprietary - All rights reserved

## Support

For issues or questions, please create a GitHub issue or contact the development team.

---

**Last Updated**: 2024
**Version**: 1.0.0
