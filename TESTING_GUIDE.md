# Testing Guide - Fixed 500 Error

## What Was Fixed

✅ **Installed psutil** - Required dependency for memory tracking  
✅ **Fixed AI metadata handling** - Code now gracefully handles when AI features are unavailable  
✅ **Added safety checks** - Metrics extraction is now robust to missing data  
✅ **Improved error messages** - Clear indication when AI features are not available  

## How to Test

### 1. **Start the Backend Server**

```bash
# Make sure you're in the project root
cd C:\Users\konda\Anomaly_Report_Project

# Start the backend (Python server)
python app.py
```

You should see:
```
================================================================================
  ANOMALY REPORT ANALYZER - BACKEND SERVER
================================================================================

✅ Backend Server Starting...
📍 Server: http://127.0.0.1:5000
📍 Frontend: http://localhost:3000
```

### 2. **Start the Frontend**

Open a **NEW terminal** and run:

```bash
cd frontend
npm start
```

The React app will open at `http://localhost:3000`

### 3. **Upload a Log File**

1. Go to `http://localhost:3000` in your browser
2. Click "Choose File" and select any `.log` or `.txt` file
3. Click "Analyze File"
4. **Check the backend terminal** - you'll see real-time metrics printed!

## Expected Output (Backend Terminal)

When you analyze a file, you'll see:

```
================================================================================
  🔍 REAL-TIME PERFORMANCE METRICS
  Timestamp: 2025-12-12 14:23:45
================================================================================

⚠️  Note: AI features not available - using standard analysis
   To enable AI metrics, install: pip install langchain-nvidia-ai-endpoints langchain-community faiss-cpu
   And set NVIDIA_API_KEY in your .env file

────────────────────────────────────────────────────────────────────────────────
  📄 File Information
────────────────────────────────────────────────────────────────────────────────
  • Filename                                 : test.log
  • File Size                                : 12345 bytes
  • Log Lines                                : 150
  • File Hash                                : a7f3e8d9c2b1f456

────────────────────────────────────────────────────────────────────────────────
  🎯 Anomaly Detection Performance
────────────────────────────────────────────────────────────────────────────────
  • Total Anomalies Detected                 : 8
  • Authentication Failures                  : 3
  • Brute Force Attacks                      : 1
  • Suspicious Sessions                      : 2
  • Resource Misconfigurations               : 1
  • Security Anomalies                       : 1

────────────────────────────────────────────────────────────────────────────────
  ⚡ End-to-End System Metrics
────────────────────────────────────────────────────────────────────────────────
  • Total Analysis Time                      : 234.5 ms
  • File Processing Latency                  : 12.3 ms
  • API Response Time                        : 246.8 ms
  • Memory Usage (estimated)                 : 145.7 MB

  ⏱️  Time Breakdown:
    - File Processing                  :    12.30 ms ( 5.0%)
    - Analysis Processing              :   234.50 ms (95.0%)

================================================================================
✅ Analysis Complete - All metrics logged
================================================================================
```

## To Enable AI Features (Optional)

If you want to see **full AI metrics** with embedding, retrieval, and LLM:

1. **Install AI libraries:**
   ```bash
   pip install langchain-nvidia-ai-endpoints langchain-community faiss-cpu
   ```

2. **Get NVIDIA API Key:**
   - Sign up at https://build.nvidia.com/
   - Get your API key

3. **Create .env file:**
   ```bash
   # In project root
   echo NVIDIA_API_KEY=your_api_key_here > .env
   ```

4. **Restart backend** and you'll see full AI metrics!

## Troubleshooting

### ❌ "Failed to load resource: 404"
- Make sure backend is running on port 5000
- Check `frontend/package.json` has `"proxy": "http://localhost:5000"`

### ❌ "Failed to load resource: 500"
- This is now fixed! But if you still see it:
  - Check backend terminal for error details
  - Make sure psutil is installed: `pip list | findstr psutil`

### ❌ Frontend won't load
- Make sure you're in the `frontend` folder
- Run `npm install` first if needed
- Check if port 3000 is available

## Success Indicators

✅ Backend shows metrics in terminal after file upload  
✅ Frontend shows analysis results  
✅ No 500 errors in browser console  
✅ Response times are displayed  
✅ Anomaly counts are shown  

Your system is now ready for testing and data collection! 🎉
