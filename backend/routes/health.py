"""
Health check routes
"""
from flask import jsonify

def register_health_routes(app, metrics):
    """Register health check routes"""
    
    @app.route('/api/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "message": "Backend is running",
            "service": "Anomaly Report Analyzer"
        }), 200
    
    @app.route('/api/metrics', methods=['GET'])
    def get_metrics():
        """Get performance metrics"""
        return jsonify(metrics.get_metrics()), 200
