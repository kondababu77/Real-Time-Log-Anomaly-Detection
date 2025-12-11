"""
Performance Metrics Model
"""
from datetime import datetime
from threading import Lock

class PerformanceMetrics:
    """Track performance metrics"""
    
    def __init__(self):
        self.lock = Lock()
        self.requests_count = 0
        self.successful_requests = 0
        self.total_response_time = 0
        self.total_processing_time = 0
        self.cache_hits = 0
        self.start_time = datetime.now()
    
    def record_request(self, success=True, response_time=0, processing_time=0):
        """Record a request metric"""
        with self.lock:
            self.requests_count += 1
            if success:
                self.successful_requests += 1
            self.total_response_time += response_time
            if processing_time > 0:
                self.total_processing_time += processing_time
    
    def record_cache_hit(self):
        """Record a cache hit"""
        with self.lock:
            self.cache_hits += 1
    
    def get_metrics(self):
        """Get current metrics"""
        with self.lock:
            uptime = (datetime.now() - self.start_time).total_seconds()
            avg_response = self.total_response_time / max(self.requests_count, 1)
            avg_processing = self.total_processing_time / max(self.requests_count, 1)
            success_rate = (self.successful_requests / max(self.requests_count, 1)) * 100
            cache_rate = (self.cache_hits / max(self.requests_count, 1)) * 100
            
            return {
                'uptime_seconds': round(uptime, 2),
                'total_requests': self.requests_count,
                'successful_requests': self.successful_requests,
                'success_rate': round(success_rate, 2),
                'avg_response_time_ms': round(avg_response, 2),
                'avg_processing_time_ms': round(avg_processing, 2),
                'cache_hit_rate': round(cache_rate, 2),
                'total_cache_hits': self.cache_hits
            }
