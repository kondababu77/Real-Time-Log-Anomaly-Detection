"""
Analysis routes
"""
import time
import os
from flask import request, jsonify
from werkzeug.utils import secure_filename
from backend.services.analyzer import LogAnalyzer
from backend.services.generator import ReportGenerator

def register_analysis_routes(app, metrics, upload_folder):
    """Register analysis routes"""
    
    @app.route('/api/analyze', methods=['POST'])
    def analyze_file():
        """Analyze uploaded file"""
        start_time = time.time()
        try:
            if 'file' not in request.files:
                metrics.record_request(success=False, response_time=(time.time() - start_time) * 1000)
                return jsonify({"error": "No file provided"}), 400
            
            file = request.files['file']
            
            if file.filename == '':
                metrics.record_request(success=False, response_time=(time.time() - start_time) * 1000)
                return jsonify({"error": "No file selected"}), 400
            
            if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in {'log', 'txt'}):
                metrics.record_request(success=False, response_time=(time.time() - start_time) * 1000)
                return jsonify({"error": "Invalid file type. Only .log and .txt allowed"}), 400
            
            # Read file content
            file_content = file.read().decode('utf-8', errors='ignore')
            
            # Generate hash
            file_hash = LogAnalyzer.get_file_hash(file_content)
            
            # Save file
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            with open(filepath, 'w') as f:
                f.write(file_content)
            
            processing_start = time.time()
            
            # Questions
            questions = [
                "Analyze anomaly in logs",
                "Find authentication failure",
                "Detect brute force attack patterns in sshd",
                "Check abnormal user sessions",
                "Find resource and configuration anomalies",
            ]
            
            # Generate reports with AI (falls back to standard if AI unavailable)
            reports = []
            for idx, question in enumerate(questions, 1):
                report = ReportGenerator.generate_report_with_ai(idx, question, file_content, file_hash, use_ai=True)
                reports.append(report)
            
            processing_time = (time.time() - processing_start) * 1000
            
            # Cleanup
            if os.path.exists(filepath):
                os.remove(filepath)
            
            response_time = (time.time() - start_time) * 1000
            metrics.record_request(success=True, response_time=response_time, processing_time=processing_time)
            
            return jsonify({
                "success": True,
                "filename": filename,
                "file_hash": file_hash[:8],
                "report_count": len(reports),
                "reports": reports,
                "metrics": {
                    "processing_time_ms": round(processing_time, 2),
                    "response_time_ms": round(response_time, 2)
                }
            }), 200
        
        except Exception as e:
            metrics.record_request(success=False, response_time=(time.time() - start_time) * 1000)
            return jsonify({"error": str(e)}), 500

    @app.route('/api/analyze-text', methods=['POST'])
    def analyze_text():
        """Analyze text directly"""
        start_time = time.time()
        try:
            data = request.get_json()
            
            if not data or 'logText' not in data:
                metrics.record_request(success=False, response_time=(time.time() - start_time) * 1000)
                return jsonify({"error": "No log text provided"}), 400
            
            log_text = data['logText'].strip()
            
            if not log_text:
                metrics.record_request(success=False, response_time=(time.time() - start_time) * 1000)
                return jsonify({"error": "Log text is empty"}), 400
            
            # Generate hash
            file_hash = LogAnalyzer.get_file_hash(log_text)
            
            processing_start = time.time()
            
            # Questions
            questions = [
                "Analyze anomaly in logs",
                "Find authentication failure",
                "Detect brute force attack patterns in sshd",
                "Check abnormal user sessions",
                "Find resource and configuration anomalies",
            ]
            
            # Generate reports with AI (falls back to standard if AI unavailable)
            reports = []
            for idx, question in enumerate(questions, 1):
                report = ReportGenerator.generate_report_with_ai(idx, question, log_text, file_hash, use_ai=True)
                reports.append(report)
            
            processing_time = (time.time() - processing_start) * 1000
            response_time = (time.time() - start_time) * 1000
            metrics.record_request(success=True, response_time=response_time, processing_time=processing_time)
            
            return jsonify({
                "success": True,
                "text_hash": file_hash[:8],
                "report_count": len(reports),
                "reports": reports,
                "metrics": {
                    "processing_time_ms": round(processing_time, 2),
                    "response_time_ms": round(response_time, 2)
                }
            }), 200
        
        except Exception as e:
            metrics.record_request(success=False, response_time=(time.time() - start_time) * 1000)
            return jsonify({"error": str(e)}), 500
