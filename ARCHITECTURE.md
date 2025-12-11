# AI-Powered Log Analysis Architecture

## 🎯 System Overview

This application uses **NVIDIA AI models** for intelligent log analysis, combining semantic search with Large Language Model (LLM) reasoning to provide accurate, evidence-based anomaly detection.

## 🤖 AI Models Stack

### 1. **nv-embedqa-e5-v5** - Semantic Embedding
- **Dimensions**: 768
- **Purpose**: Convert log text → semantic vectors
- **Why**: Understands meaning beyond keywords

### 2. **Llama 3.1-70B** - LLM Reasoning  
- **Temperature**: 0.1 (factual)
- **Purpose**: Root cause analysis
- **Why**: Evidence-grounded insights (no hallucination)

### 3. **FAISS** - Vector Search
- **Complexity**: O(1)
- **Purpose**: Fast similarity search
- **Why**: Instant retrieval from thousands of logs

### 4. **RecursiveTextSplitter** - Chunking
- **Chunk Size**: 500 chars
- **Overlap**: 50 chars
- **Purpose**: Preserve log context

## 📊 Processing Pipeline

```
User Upload Log
    ↓
[1] RecursiveTextSplitter → chunks
    ↓
[2] nv-embedqa-e5-v5 → 768-dim vectors
    ↓  
[3] FAISS → indexed vectors
    ↓
[4] Semantic Search → top-4 relevant chunks
    ↓
[5] Llama 3.1 → root cause + actions
    ↓
Structured Report
```

## ⚡ Performance

- **Text Chunking**: ~50ms
- **Embedding**: ~200ms
- **FAISS Indexing**: ~10ms
- **Similarity Search**: ~5ms
- **LLM Analysis**: ~2-3s
- **Total**: ~3-4s per file

## 🛡️ Fallback System

```
AI Available? 
  ├─ YES → Use AI Pipeline
  └─ NO  → Rule-Based Analysis (still works!)
```

**See full details in AI_SETUP_GUIDE.md**
