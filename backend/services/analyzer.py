"""
Log Analyzer Service - Processes log content
"""
import hashlib

class LogAnalyzer:
    """Analyzes log file content and generates statistics"""
    
    @staticmethod
    def extract_log_stats(content):
        """Extract statistics from log content"""
        lines = content.split('\n')
        
        stats = {
            'total_lines': len([l for l in lines if l.strip()]),
            'error_count': len([l for l in lines if 'error' in l.lower()]),
            'warning_count': len([l for l in lines if 'warning' in l.lower()]),
            'failed_count': len([l for l in lines if 'failed' in l.lower()]),
            'timeout_count': len([l for l in lines if 'timeout' in l.lower()]),
            'ssh_count': len([l for l in lines if 'ssh' in l.lower()]),
            'auth_count': len([l for l in lines if 'auth' in l.lower()]),
            'connection_count': len([l for l in lines if 'connection' in l.lower()]),
            'denied_count': len([l for l in lines if 'denied' in l.lower()]),
            'accepted_count': len([l for l in lines if 'accepted' in l.lower()]),
        }
        
        error_lines = [l.strip()[:100] for l in lines if 'error' in l.lower()][:3]
        warning_lines = [l.strip()[:100] for l in lines if 'warning' in l.lower()][:3]
        
        return stats, error_lines, warning_lines
    
    @staticmethod
    def get_file_hash(content):
        """Generate hash of file content"""
        return hashlib.md5(content.encode()).hexdigest()
