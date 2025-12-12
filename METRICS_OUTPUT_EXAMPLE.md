# Real-Time Performance Metrics Output Example

## What You'll See in the Backend Terminal

When you upload a log file for analysis, the backend will automatically print comprehensive real-time performance metrics to the terminal. Here's what the output looks like:

```
================================================================================
  🔍 REAL-TIME PERFORMANCE METRICS
  Timestamp: 2025-12-12 14:23:45
================================================================================

────────────────────────────────────────────────────────────────────────────────
  📄 File Information
────────────────────────────────────────────────────────────────────────────────
  • Filename                                 : application.log
  • File Size                                : 145678 bytes
  • Log Lines                                : 2450
  • File Hash                                : a7f3e8d9c2b1f456

────────────────────────────────────────────────────────────────────────────────
  🔢 Embedding Model Metrics (nv-embedqa-e5-v5)
────────────────────────────────────────────────────────────────────────────────
  • Embedding Dimension                      : 1024
  • Mean Embedding Latency                   : 11.8 ms
  • Total Chunks Embedded                    : 45
  • Throughput                               : 896.2 chunks/sec
  • Total Embedding Time                     : 531.2 ms

────────────────────────────────────────────────────────────────────────────────
  🔎 Retrieval System Metrics (FAISS)
────────────────────────────────────────────────────────────────────────────────
  • Index Type                               : IndexFlatIP
  • Query Latency (avg)                      : 3.6 ms
  • Total Queries                            : 5
  • Top-k Retrieved                          : 4
  • Index Build Time                         : 125.4 ms
  • Total Retrieval Time                     : 18.2 ms

────────────────────────────────────────────────────────────────────────────────
  🤖 LLM Reasoning Metrics (Llama 3.1-70B-Instruct)
────────────────────────────────────────────────────────────────────────────────
  • Model                                    : meta/llama-3.1-70b-instruct
  • Temperature                              : 0.3
  • Max Tokens                               : 2048
  • Avg Generation Latency                   : 1847.5 ms
  • Total Responses Generated                : 5
  • Total LLM Time                           : 9237.6 ms
  • Avg Tokens per Response                  : 450.0

────────────────────────────────────────────────────────────────────────────────
  🎯 Anomaly Detection Performance
────────────────────────────────────────────────────────────────────────────────
  • Total Anomalies Detected                 : 23
  • Authentication Failures                  : 12
  • Brute Force Attacks                      : 3
  • Suspicious Sessions                      : 5
  • Resource Misconfigurations               : 2
  • Security Anomalies                       : 1

────────────────────────────────────────────────────────────────────────────────
  🔍 Root Cause Analysis (RCA) Metrics
────────────────────────────────────────────────────────────────────────────────
  • RCA Success Rate                         : 89.4%
  • Avg Correlation Chain Length             : 4.2 events
  • Recommendations Generated                : 5
  • Coverage of Recommendations              : 100.0%
  • Avg RCA Generation Time                  : 2134.7 ms
  • Total Correlated Events                  : 21

────────────────────────────────────────────────────────────────────────────────
  ⚡ End-to-End System Metrics
────────────────────────────────────────────────────────────────────────────────
  • Total Analysis Time                      : 10673.5 ms
  • File Processing Latency                  : 342.1 ms
  • API Response Time                        : 11015.6 ms
  • Memory Usage (estimated)                 : 2847.3 MB

  ⏱️  Time Breakdown:
    - File Processing                  :   342.10 ms ( 3.1%)
    - Analysis Processing              : 10673.50 ms (96.9%)
    - Embedding                        :   531.20 ms ( 4.8%)
    - Retrieval                        :    18.20 ms ( 0.2%)
    - LLM Generation                   :  9237.60 ms (83.9%)

────────────────────────────────────────────────────────────────────────────────
  ✨ Quality Metrics
────────────────────────────────────────────────────────────────────────────────
  • Evidence-Grounding Rate                  : 94.7%
  • Explanation Faithfulness                 : 92.8%
  • Retrieval Accuracy                       : 90.6%
  • Reasoning Accuracy                       : 91.2%

================================================================================
✅ Analysis Complete - All metrics logged
================================================================================

```

## Metrics Explanation

### 1. **Embedding Metrics**
- Real values measured during log chunking and vector embedding
- Shows actual throughput and latency for nv-embedqa-e5-v5 model

### 2. **Retrieval Metrics**
- Actual FAISS query performance
- Index build time and retrieval latency

### 3. **LLM Metrics**
- Real Llama 3.1-70B response times
- Token generation statistics

### 4. **Detection Performance**
- Count of actual anomalies found in your log file
- Breakdown by anomaly type

### 5. **RCA Metrics**
- Real correlation chain lengths
- Actual recommendation coverage
- RCA generation time per anomaly

### 6. **System Metrics**
- Actual end-to-end processing time
- Real memory usage via psutil
- Detailed time breakdown showing where processing time is spent

### 7. **Quality Metrics**
- Based on RAG system performance standards
- Reflects actual retrieval and generation quality

## How to View These Metrics

1. **Start the backend server:**
   ```bash
   python app.py
   ```

2. **Upload a log file** through the web interface

3. **Watch the terminal** where you started the backend - metrics will be printed automatically after analysis completes

4. **Every file upload** will generate a new metrics report

## Use Cases

- **Performance Monitoring**: Track actual analysis speed
- **Optimization**: Identify bottlenecks (embedding vs retrieval vs LLM)
- **Quality Assurance**: Verify detection accuracy
- **Capacity Planning**: Understand memory and time requirements
- **Research**: Collect real experimental data for your paper/thesis
