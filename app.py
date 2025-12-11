"""
Main Application - Anomaly Report Analyzer Backend
Clean modular architecture
"""
import os
import sys

# Ensure UTF-8 encoding for Windows
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from flask import Flask
from flask_cors import CORS

# Import models, services, and routes
from backend.models import PerformanceMetrics
from backend.routes import register_health_routes, register_analysis_routes
from backend.utils import ensure_upload_folder

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'log', 'txt'}
MAX_FILE_SIZE = 50 * 1024 * 1024

# Create Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.config['JSON_SORT_KEYS'] = False

# Ensure upload folder exists
ensure_upload_folder(UPLOAD_FOLDER)

# Initialize metrics
metrics = PerformanceMetrics()

# Register routes
register_health_routes(app, metrics)
register_analysis_routes(app, metrics, UPLOAD_FOLDER)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  ANOMALY REPORT ANALYZER - BACKEND SERVER")
    print("="*70)
    print("\n✅ Backend Server Starting...")
    print("📍 Server: http://127.0.0.1:5000")
    print("📍 Frontend: http://localhost:3000")
    print("\n✨ Endpoints:")
    print("   • GET  /api/health - Health check")
    print("   • POST /api/analyze - Upload and analyze file")
    print("   • POST /api/analyze-text - Analyze text")
    print("   • GET  /api/metrics - Performance metrics")
    print("\n📊 Features:")
    print("   ✓ File content analysis")
    print("   ✓ Context-aware reports")
    print("   ✓ Real-time metrics")
    print("   ✓ Batch processing")
    print("\n📁 Architecture:")
    print("   models/     - Data models")
    print("   services/   - Business logic")
    print("   routes/     - API endpoints")
    print("   utils/      - Helper functions")
    print("\n" + "="*70 + "\n")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False, threaded=True)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()
