"""
Performance Metrics Printer - Displays real-time analysis metrics
"""
import time
from datetime import datetime
from typing import Dict, List, Any


class MetricsPrinter:
    """Prints comprehensive performance metrics to console"""
    
    @staticmethod
    def print_separator(char="=", length=80):
        """Print a separator line"""
        print(char * length)
    
    @staticmethod
    def print_header(title: str):
        """Print a formatted header"""
        MetricsPrinter.print_separator()
        print(f"  {title}")
        print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        MetricsPrinter.print_separator()
    
    @staticmethod
    def print_section(title: str):
        """Print a section title"""
        print(f"\n{'─' * 80}")
        print(f"  {title}")
        print(f"{'─' * 80}")
    
    @staticmethod
    def print_metric(name: str, value: Any, unit: str = ""):
        """Print a single metric"""
        value_str = f"{value} {unit}".strip() if unit else str(value)
        print(f"  • {name:<40} : {value_str}")
    
    @staticmethod
    def print_analysis_metrics(metrics_data: Dict[str, Any]):
        """Print comprehensive analysis metrics"""
        
        MetricsPrinter.print_header("🔍 REAL-TIME PERFORMANCE METRICS")
        
        # Check if AI features are available
        has_ai_metrics = (metrics_data.get('embedding_metrics') or 
                         metrics_data.get('retrieval_metrics') or 
                         metrics_data.get('llm_metrics'))
        
        if not has_ai_metrics:
            print("\n⚠️  Note: AI features not available - using standard analysis")
            print("   To enable AI metrics, install: pip install langchain-nvidia-ai-endpoints langchain-community faiss-cpu")
            print("   And set NVIDIA_API_KEY in your .env file\n")
        
        # File Information
        if 'file_info' in metrics_data:
            MetricsPrinter.print_section("📄 File Information")
            file_info = metrics_data['file_info']
            MetricsPrinter.print_metric("Filename", file_info.get('filename', 'N/A'))
            MetricsPrinter.print_metric("File Size", file_info.get('size', 0), "bytes")
            MetricsPrinter.print_metric("Log Lines", file_info.get('lines', 0))
            MetricsPrinter.print_metric("File Hash", file_info.get('hash', 'N/A'))
        
        # 1. Embedding Model Metrics
        if 'embedding_metrics' in metrics_data and metrics_data['embedding_metrics']:
            MetricsPrinter.print_section("🔢 Embedding Model Metrics (nv-embedqa-e5-v5)")
            emb = metrics_data['embedding_metrics']
            MetricsPrinter.print_metric("Embedding Dimension", emb.get('dimension', 1024))
            MetricsPrinter.print_metric("Mean Embedding Latency", round(emb.get('latency_ms', 0), 2), "ms")
            MetricsPrinter.print_metric("Total Chunks Embedded", emb.get('chunks_embedded', 0))
            MetricsPrinter.print_metric("Throughput", round(emb.get('throughput', 0), 2), "chunks/sec")
            MetricsPrinter.print_metric("Total Embedding Time", round(emb.get('total_time_ms', 0), 2), "ms")
        
        # 2. Retrieval System Metrics
        if 'retrieval_metrics' in metrics_data and metrics_data['retrieval_metrics']:
            MetricsPrinter.print_section("🔎 Retrieval System Metrics (FAISS)")
            ret = metrics_data['retrieval_metrics']
            MetricsPrinter.print_metric("Index Type", ret.get('index_type', 'IndexFlatIP'))
            MetricsPrinter.print_metric("Query Latency (avg)", round(ret.get('avg_query_latency_ms', 0), 2), "ms")
            MetricsPrinter.print_metric("Total Queries", ret.get('total_queries', 0))
            MetricsPrinter.print_metric("Top-k Retrieved", ret.get('top_k', 4))
            MetricsPrinter.print_metric("Index Build Time", round(ret.get('index_build_time_ms', 0), 2), "ms")
            MetricsPrinter.print_metric("Total Retrieval Time", round(ret.get('total_retrieval_time_ms', 0), 2), "ms")
        
        # 3. LLM Reasoning Metrics
        if 'llm_metrics' in metrics_data and metrics_data['llm_metrics']:
            MetricsPrinter.print_section("🤖 LLM Reasoning Metrics (Llama 3.1-70B-Instruct)")
            llm = metrics_data['llm_metrics']
            MetricsPrinter.print_metric("Model", llm.get('model', 'meta/llama-3.1-70b-instruct'))
            MetricsPrinter.print_metric("Temperature", llm.get('temperature', 0.3))
            MetricsPrinter.print_metric("Max Tokens", llm.get('max_tokens', 2048))
            MetricsPrinter.print_metric("Avg Generation Latency", round(llm.get('avg_latency_ms', 0), 2), "ms")
            MetricsPrinter.print_metric("Total Responses Generated", llm.get('total_responses', 0))
            MetricsPrinter.print_metric("Total LLM Time", round(llm.get('total_time_ms', 0), 2), "ms")
            MetricsPrinter.print_metric("Avg Tokens per Response", round(llm.get('avg_tokens', 0), 1))
        
        # 4. Detection Performance
        if 'detection_metrics' in metrics_data:
            MetricsPrinter.print_section("🎯 Anomaly Detection Performance")
            det = metrics_data['detection_metrics']
            MetricsPrinter.print_metric("Total Anomalies Detected", det.get('total_anomalies', 0))
            MetricsPrinter.print_metric("Authentication Failures", det.get('auth_failures', 0))
            MetricsPrinter.print_metric("Brute Force Attacks", det.get('brute_force', 0))
            MetricsPrinter.print_metric("Suspicious Sessions", det.get('suspicious_sessions', 0))
            MetricsPrinter.print_metric("Resource Misconfigurations", det.get('misconfigurations', 0))
            MetricsPrinter.print_metric("Security Anomalies", det.get('security_anomalies', 0))
        
        # 5. Root Cause Analysis (RCA) Metrics
        if 'rca_metrics' in metrics_data and metrics_data['rca_metrics']:
            MetricsPrinter.print_section("🔍 Root Cause Analysis (RCA) Metrics")
            rca = metrics_data['rca_metrics']
            MetricsPrinter.print_metric("RCA Success Rate", f"{round(rca.get('success_rate', 0) * 100, 1)}%")
            MetricsPrinter.print_metric("Avg Correlation Chain Length", round(rca.get('avg_chain_length', 0), 1), "events")
            MetricsPrinter.print_metric("Recommendations Generated", rca.get('recommendations_count', 0))
            MetricsPrinter.print_metric("Coverage of Recommendations", f"{round(rca.get('recommendation_coverage', 0) * 100, 1)}%")
            MetricsPrinter.print_metric("Avg RCA Generation Time", round(rca.get('avg_generation_time_ms', 0), 2), "ms")
            MetricsPrinter.print_metric("Total Correlated Events", rca.get('total_correlated_events', 0))
        
        # 6. End-to-End System Metrics
        if 'system_metrics' in metrics_data:
            MetricsPrinter.print_section("⚡ End-to-End System Metrics")
            sys_met = metrics_data['system_metrics']
            MetricsPrinter.print_metric("Total Analysis Time", round(sys_met.get('total_time_ms', 0), 2), "ms")
            MetricsPrinter.print_metric("File Processing Latency", round(sys_met.get('file_processing_ms', 0), 2), "ms")
            MetricsPrinter.print_metric("API Response Time", round(sys_met.get('response_time_ms', 0), 2), "ms")
            MetricsPrinter.print_metric("Memory Usage (estimated)", round(sys_met.get('memory_mb', 0), 1), "MB")
            
            # Time breakdown
            if 'time_breakdown' in sys_met:
                print(f"\n  ⏱️  Time Breakdown:")
                breakdown = sys_met['time_breakdown']
                total = sys_met.get('total_time_ms', 1)
                for phase, duration in breakdown.items():
                    percentage = (duration / total) * 100 if total > 0 else 0
                    print(f"    - {phase:<35} : {round(duration, 2):>8.2f} ms ({round(percentage, 1):>5.1f}%)")
        
        # 7. Quality Metrics
        if 'quality_metrics' in metrics_data:
            MetricsPrinter.print_section("✨ Quality Metrics")
            qual = metrics_data['quality_metrics']
            MetricsPrinter.print_metric("Evidence-Grounding Rate", f"{round(qual.get('evidence_grounding', 0) * 100, 1)}%")
            MetricsPrinter.print_metric("Explanation Faithfulness", f"{round(qual.get('faithfulness', 0) * 100, 1)}%")
            MetricsPrinter.print_metric("Retrieval Accuracy", f"{round(qual.get('retrieval_accuracy', 0) * 100, 1)}%")
            MetricsPrinter.print_metric("Reasoning Accuracy", f"{round(qual.get('reasoning_accuracy', 0) * 100, 1)}%")
        
        MetricsPrinter.print_separator()
        print(f"✅ Analysis Complete - All metrics logged")
        MetricsPrinter.print_separator()
        print()
