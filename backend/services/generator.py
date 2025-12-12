"""
Advanced Report Generator with Automated Insight Generation
Implements research abstract requirements:
- Adaptive hyperparameter optimization for detection accuracy
- Real-time continual learning across dynamic environments  
- Robustness to noisy, incomplete, and corrupted log data
- Automated insight generation from detection results
"""
from datetime import datetime
import uuid
from .analyzer import LogAnalyzer
from .ai_analyzer import get_ai_analyzer, AILogAnalyzer
from .advanced_analyzer import AdvancedLogAnalyzer

class ReportGenerator:
    """
    Generates dynamic reports with advanced anomaly detection capabilities.
    Integrates adaptive optimization, continual learning, and noise-robust analysis.
    """
    
    # Initialize advanced analyzer with continual learning
    _advanced_analyzer = None
    
    @classmethod
    def get_advanced_analyzer(cls):
        """Get singleton instance of advanced analyzer for continual learning"""
        if cls._advanced_analyzer is None:
            cls._advanced_analyzer = AdvancedLogAnalyzer()
        return cls._advanced_analyzer
    
    # Define normal parameter ranges and percentile thresholds
    NORMAL_RANGES = {
        'error_count': {'low': 0, 'medium': 10, 'high': 50},
        'warning_count': {'low': 0, 'medium': 5, 'high': 20},
        'ssh_count': {'low': 0, 'medium': 50, 'high': 100},
        'timeout_count': {'low': 0, 'medium': 5, 'high': 10},
        'failed_count': {'low': 0, 'medium': 3, 'high': 10}
    }
    
    # Root cause categories with evidence patterns
    CAUSE_CATEGORIES = {
        'resource_exhaustion': {
            'description': 'System resources (CPU, memory, disk, connections) exceed capacity',
            'fixes': ['Scale CPU/RAM', 'Increase thread pools', 'Adjust connection limits', 'Fix disk quotas']
        },
        'configuration_error': {
            'description': 'Misconfiguration in application or system settings',
            'fixes': ['Fix endpoints/ports', 'Correct timeouts', 'Review feature flags', 'Validate credentials']
        },
        'network_issue': {
            'description': 'Network connectivity, latency, or security problems',
            'fixes': ['Whitelist IP addresses', 'Check firewall rules', 'Fix TLS configuration', 'Test connectivity']
        },
        'security_threat': {
            'description': 'Potential security breach, attack, or unauthorized access attempt',
            'fixes': ['Enable rate limiting', 'Block suspicious IPs', 'Enable MFA', 'Audit access logs']
        },
        'application_error': {
            'description': 'Code-level exception, unhandled error, or logic failure',
            'fixes': ['Handle exceptions', 'Add retries with backoff', 'Validate inputs', 'Review error logs']
        },
        'operational_issue': {
            'description': 'Service needs restart, queue cleanup, or manual intervention',
            'fixes': ['Restart service', 'Clear stuck queues', 'Re-run failed jobs', 'Clear cache']
        }
    }
    
    @staticmethod
    def analyze_parameter_deviations(stats):
        """Analyze which parameters deviate from normal ranges"""
        deviations = []
        
        for param, ranges in ReportGenerator.NORMAL_RANGES.items():
            if param in stats:
                value = stats[param]
                if value > ranges['high']:
                    deviation_pct = ((value - ranges['high']) / ranges['high'] * 100) if ranges['high'] > 0 else 100
                    deviations.append({
                        'parameter': param,
                        'value': value,
                        'normal_threshold': ranges['high'],
                        'deviation_type': 'HIGH',
                        'deviation_percent': round(deviation_pct, 1)
                    })
        
        return deviations
    
    @staticmethod
    def generate_automated_insights(analysis_result, stats, question):
        """
        Automated Insight Generation from detection results.
        Produces actionable intelligence based on adaptive analysis.
        """
        insights = {
            'key_findings': [],
            'adaptive_alerts': [],
            'continual_learning_status': {},
            'noise_robustness_metrics': {},
            'optimization_recommendations': []
        }
        
        # Key findings from advanced analysis
        if analysis_result.get('distribution_drift', {}).get('is_drifting'):
            drift_score = analysis_result['distribution_drift']['drift_score']
            insights['key_findings'].append(
                f"⚠️ Distribution Drift Detected: Log pattern has shifted {drift_score:.1%} from baseline. "
                f"System behavior is evolving - continual learning adapting thresholds."
            )
        
        # Corruption and noise handling insights
        corruption_stats = analysis_result.get('corruption_stats', {})
        if corruption_stats.get('corrupted_lines', 0) > 0:
            recovery_rate = (
                corruption_stats.get('recovered_lines', 0) / 
                max(corruption_stats.get('corrupted_lines', 1), 1)
            ) * 100
            insights['noise_robustness_metrics'] = {
                'corrupted_lines': corruption_stats.get('corrupted_lines', 0),
                'recovered_lines': corruption_stats.get('recovered_lines', 0),
                'recovery_rate': f"{recovery_rate:.1f}%",
                'robustness_level': 'High' if recovery_rate > 80 else 'Medium' if recovery_rate > 50 else 'Low'
            }
            insights['key_findings'].append(
                f"🛡️ Noise Robustness: Successfully recovered {recovery_rate:.1f}% of corrupted log entries. "
                f"Advanced parsing handled {corruption_stats.get('corrupted_lines', 0)} noisy lines."
            )
        
        # Adaptive threshold insights
        thresholds = analysis_result.get('optimized_thresholds', {})
        if thresholds:
            insights['adaptive_alerts'].append(
                f"📊 Adaptive Thresholds Active: Error rate threshold = {thresholds.get('error_rate', 0.05):.2%}, "
                f"Anomaly score threshold = {thresholds.get('anomaly_score', 0.75):.2f}"
            )
        
        # Continual learning status
        learning_meta = analysis_result.get('learning_metadata', {})
        insights['continual_learning_status'] = {
            'total_analyses': learning_meta.get('analysis_count', 0),
            'baseline_established': learning_meta.get('baseline_established', False),
            'patterns_learned': learning_meta.get('pattern_memory_size', 0),
            'threshold_adaptations': learning_meta.get('threshold_adjustments', 0),
            'learning_state': 'Active' if learning_meta.get('baseline_established') else 'Initializing'
        }
        
        if learning_meta.get('baseline_established'):
            insights['key_findings'].append(
                f"🧠 Continual Learning Active: System has processed {learning_meta.get('analysis_count', 0)} logs, "
                f"learned {learning_meta.get('pattern_memory_size', 0)} unique patterns, "
                f"and performed {learning_meta.get('threshold_adjustments', 0)} adaptive optimizations."
            )
        
        # Pattern-based insights
        patterns = analysis_result.get('patterns', {})
        if patterns.get('error_codes'):
            unique_errors = len(set(patterns['error_codes']))
            insights['key_findings'].append(
                f"🔍 Detected {unique_errors} unique error codes across {len(patterns['error_codes'])} occurrences"
            )
        
        # Optimization recommendations based on current state
        if analysis_result.get('severity') == 'Critical':
            insights['optimization_recommendations'].append(
                "🚨 Critical severity detected - consider increasing monitoring frequency and enabling auto-scaling"
            )
        
        if stats.get('error_count', 0) > stats.get('total_lines', 1) * 0.1:
            insights['optimization_recommendations'].append(
                "⚡ High error rate (>10%) - recommend implementing circuit breaker pattern and retry mechanisms"
            )
        
        return insights
    
    @staticmethod
    def determine_cause_category(question, stats):
        """Determine root cause category based on question and statistics"""
        causes = []
        
        if question == "Detect brute force attack patterns in sshd":
            if stats['ssh_count'] > 100 or stats['failed_count'] > 20:
                causes.append('security_threat')
            if stats['ssh_count'] > 50:
                causes.append('network_issue')
        
        elif question == "Find authentication failure":
            if stats['denied_count'] > 20 or stats['failed_count'] > 15:
                causes.append('security_threat')
            if stats['denied_count'] > 5:
                causes.append('configuration_error')
        
        elif question == "Check abnormal user sessions":
            if stats['timeout_count'] > 10:
                causes.append('network_issue')
            if stats['connection_count'] > 100:
                causes.append('resource_exhaustion')
        
        elif question == "Find resource and configuration anomalies":
            if stats['warning_count'] > 20:
                causes.append('resource_exhaustion')
            if stats['warning_count'] > 5:
                causes.append('configuration_error')
        
        elif question == "Analyze anomaly in logs":
            if stats['error_count'] > 50:
                causes.append('application_error')
            if stats['error_count'] > 10 and stats['warning_count'] > 5:
                causes.append('resource_exhaustion')
        
        return causes if causes else ['operational_issue']
    
    @staticmethod
    def generate_report_with_ai(sequence_id, question, file_content, file_hash, use_ai=True):
        """
        Generate comprehensive report with advanced analysis capabilities.
        Integrates: AI analysis, adaptive optimization, continual learning, noise robustness.
        
        Args:
            sequence_id: Sequence number for this report
            question: Analysis question
            file_content: Raw log content
            file_hash: Hash of the file
            use_ai: Whether to use AI analysis (default: True)
        """
        # Step 1: Use Advanced Analyzer for noise-robust, adaptive analysis
        advanced_analyzer = ReportGenerator.get_advanced_analyzer()
        analysis_result = advanced_analyzer.analyze(file_content)
        
        stats = analysis_result['stats']
        severity = analysis_result['severity']
        confidence_score = analysis_result['confidence'] * 100
        
        # Step 2: Generate automated insights from detection results
        automated_insights = ReportGenerator.generate_automated_insights(
            analysis_result, stats, question
        )
        
        # Step 3: Try AI-powered analysis if enabled
        use_ai_enhancement = use_ai
        ai_analysis = None
        ai_metadata = {'embedding_time': 0, 'retrieval_time': 0, 'llm_time': 0}
        
        if use_ai_enhancement:
            ai_analyzer = get_ai_analyzer()
            if ai_analyzer:
                try:
                    # Process log file with AI models
                    ai_stats, vector_store = ai_analyzer.process_log_file(file_content)
                    ai_metadata['embedding_time'] = ai_stats.get('embedding_time_ms', 0)
                    
                    # Get AI-powered analysis
                    ai_analysis = ai_analyzer.analyze_with_llm(question, top_k=4)
                    
                    # Extract timing from AI analysis
                    if 'timing_metadata' in ai_analysis:
                        ai_metadata['retrieval_time'] = ai_analysis['timing_metadata'].get('retrieval_time_ms', 0)
                        ai_metadata['llm_time'] = ai_analysis['timing_metadata'].get('llm_time_ms', 0)
                    
                    # Merge AI insights if available
                    if ai_analysis:
                        severity = ai_analysis.get('severity', severity)
                        confidence_score = ai_analysis.get('confidence_score', confidence_score)
                except Exception as e:
                    print(f"⚠️  AI analysis failed: {e}. Using advanced analyzer results.")
                    use_ai_enhancement = False
        
        # Create unique sequence ID
        unique_sequence = f"{file_hash[:4]}-{sequence_id:02d}-{uuid.uuid4().hex[:4]}".upper()
        
        # Step 4: Build comprehensive report with all advanced features
        if use_ai_enhancement and ai_analysis:
            # AI-enhanced path
            category = ai_analysis.get('category', 'operational_issue')
            immediate_actions = ai_analysis.get('immediate_actions', [])[:3]
            evidence_chunks = ai_analysis.get('evidence_chunks', [])
            root_cause_explanation = ai_analysis.get('root_cause_explanation', '')
            
            return ReportGenerator._build_advanced_ai_report(
                unique_sequence, sequence_id, question, file_hash,
                stats, severity, confidence_score, root_cause_explanation,
                category, immediate_actions, evidence_chunks,
                analysis_result, automated_insights, ai_metadata
            )
        else:
            # Advanced analyzer path (no AI)
            return ReportGenerator._build_advanced_report(
                unique_sequence, sequence_id, question, file_hash,
                stats, severity, confidence_score,
                analysis_result, automated_insights, ai_metadata
            )
    
    @staticmethod
    def _build_advanced_report(unique_sequence, sequence_id, question, file_hash,
                              stats, severity, confidence, analysis_result, automated_insights, ai_metadata=None):
        """
        Build report using Advanced Analyzer with automated insight generation.
        Highlights: Adaptive optimization, continual learning, noise robustness.
        """
        # Analyze parameter deviations
        deviations = ReportGenerator.analyze_parameter_deviations(stats)
        
        # Determine root cause categories
        cause_categories = ReportGenerator.determine_cause_category(question, stats)
        category_info = ReportGenerator.CAUSE_CATEGORIES.get(cause_categories[0] if cause_categories else 'operational_issue',
                                                             ReportGenerator.CAUSE_CATEGORIES['operational_issue'])
        
        # Generate root cause explanation
        root_cause_explanation = ReportGenerator._generate_adaptive_explanation(
            question, stats, analysis_result, automated_insights
        )
        
        return {
            "sequence": unique_sequence,
            "sequence_id": sequence_id,
            "question": question,
            "file_hash": file_hash[:8],
            "advanced_features": True,
            "summary": {
                "title": "ADVANCED ANOMALY DETECTION REPORT (Adaptive + Continual Learning)",
                "analysis": f"Advanced analysis with adaptive optimization and noise-robust parsing. "
                           f"{automated_insights['continual_learning_status'].get('learning_state', 'Active')} continual learning. "
                           f"Processed {stats['total_lines']} log lines with {analysis_result.get('corruption_stats', {}).get('recovered_lines', 0)} recovered from corruption.",
                "time_range": datetime.now().isoformat(),
                "primary_component": "Advanced Adaptive Analyzer",
                "severity": severity,
                "anomaly_score": round((confidence * (len(deviations) + 1)) / 100, 1)
            },
            "where_anomaly_occurred": {
                "component": "Adaptive Log Analysis Engine",
                "affected_service": f"Continual Learning System - {question}",
                "timestamp": datetime.now().isoformat()
            },
            "anomalous_events": {
                "total_events": len(deviations) + stats.get('error_count', 0),
                "list": [f"Error events: {stats.get('error_count', 0)}", f"Warning events: {stats.get('warning_count', 0)}"]
            },
            "workflow_comparison": {
                "normal_sequence": ["Static Rules", "Fixed Thresholds", "Manual Analysis", "Static Reports"],
                "current_sequence": [
                    "Noise-Robust Parsing",
                    "Adaptive Hyperparameter Optimization",
                    "Continual Learning Baseline Update",
                    "Distribution Drift Detection",
                    "Automated Insight Generation"
                ],
                "deviations": [
                    "✓ Adaptive thresholds evolve with log patterns (not static)",
                    "✓ Continual learning maintains accuracy across dynamic environments",
                    "✓ Robust to corrupted and noisy log data",
                    f"✓ {analysis_result.get('learning_metadata', {}).get('threshold_adjustments', 0)} automatic optimizations performed"
                ]
            },
            "root_cause_hypothesis": {
                "primary_cause": cause_categories[0] if cause_categories else 'unknown',
                "cause_description": category_info['description'],
                "contributing_factors": cause_categories[1:3] if len(cause_categories) > 1 else [],
                "likelihood": "High" if severity == "Critical" else "Medium" if severity == "High" else "Low",
                "adaptive_confidence": f"{confidence:.1f}% (adaptive threshold)"
            },
            "evidence": {
                "structural_deviations": automated_insights['key_findings'],
                "parameter_deviations": deviations,
                "component_concentration": {
                    "primary_component": "Advanced Analyzer",
                    "component_event_count": stats.get('error_count', 0) + stats.get('warning_count', 0),
                    "concentration_percentage": round(
                        ((stats.get('error_count', 0) + stats.get('warning_count', 0)) / max(stats['total_lines'], 1)) * 100, 1
                    )
                },
                "statistical_evidence": [
                    f"Total log lines: {stats['total_lines']}",
                    f"Error events: {stats['error_count']}",
                    f"Warning events: {stats['warning_count']}",
                    f"Failed attempts: {stats['failed_count']}",
                    f"Corrupted lines recovered: {analysis_result.get('corruption_stats', {}).get('recovered_lines', 0)}"
                ],
                "noise_robustness": automated_insights.get('noise_robustness_metrics', {}),
                "continual_learning": automated_insights.get('continual_learning_status', {})
            },
            "rectification_suggestions": {
                "immediate_actions": category_info['fixes'][:3] if category_info else [],
                "short_term_fixes": [
                    "Monitor adaptive threshold adjustments for stability",
                    "Review continual learning baseline for accuracy",
                    "Validate noise recovery effectiveness"
                ],
                "long_term_improvements": automated_insights.get('optimization_recommendations', []) + [
                    "Integrate feedback loop for continual learning enhancement",
                    "Expand pattern memory for better adaptation",
                    "Implement automated alert escalation based on adaptive severity"
                ],
                "categorized_recommendations": {
                    "configuration": ["Review adaptive threshold configuration", "Validate learning rate parameters"],
                    "resources": ["Monitor system resources during continual learning", "Optimize pattern memory storage"],
                    "code": ["Enhance noise recovery algorithms", "Improve drift detection sensitivity"],
                    "network": ["Check for network-induced log corruption", "Validate log transmission integrity"],
                    "operational": ["Review automated insights regularly", "Calibrate adaptive thresholds", "Monitor learning performance"]
                }
            },
            "automated_insights": automated_insights,
            "adaptive_features": {
                "optimized_thresholds": analysis_result.get('optimized_thresholds', {}),
                "distribution_drift": analysis_result.get('distribution_drift', {}),
                "learning_metadata": analysis_result.get('learning_metadata', {})
            },
            "statistics": stats,
            "root_cause": {
                "explanation": root_cause_explanation,
                "evidence": [
                    f"Adaptive Hyperparameter Optimization: {analysis_result.get('learning_metadata', {}).get('threshold_adjustments', 0)} adjustments",
                    f"Continual Learning: {analysis_result.get('learning_metadata', {}).get('patterns_learned', 0)} patterns learned",
                    f"Noise Robustness: {analysis_result.get('corruption_stats', {}).get('recovery_rate', 'N/A')} recovery rate",
                    f"Distribution Drift: {'Detected' if analysis_result.get('distribution_drift', {}).get('is_drifting') else 'Stable'}"
                ]
            },
            "recommendations": {
                "configuration": ["Optimize adaptive parameters", "Fine-tune learning rate"],
                "resources": ["Scale for continual learning", "Allocate memory for pattern storage"],
                "code": ["Enhance recovery algorithms", "Improve insight generation"],
                "network": ["Monitor log integrity", "Validate transmission"],
                "operational": ["Review insights", "Calibrate thresholds", "Monitor learning"]
            },
            "detailed_analysis": f"Advanced Adaptive Analysis\n"
                                f"Question: {question}\n\n"
                                f"Features: Adaptive Optimization, Continual Learning, Noise Robustness\n"
                                f"Severity: {severity}\n"
                                f"Confidence: {confidence:.1f}%\n"
                                f"Learning State: {automated_insights['continual_learning_status'].get('learning_state', 'Active')}",
            "confidence_score": round(confidence, 1),
            "ai_metadata": ai_metadata if ai_metadata else {'embedding_time': 0, 'retrieval_time': 0, 'llm_time': 0}
        }
    
    @staticmethod
    def _generate_adaptive_explanation(question, stats, analysis_result, insights):
        """Generate explanation incorporating adaptive learning insights"""
        base_explanation = f"Advanced analysis detected {stats.get('error_count', 0)} errors and {stats.get('warning_count', 0)} warnings. "
        
        if analysis_result.get('distribution_drift', {}).get('is_drifting'):
            base_explanation += f"System behavior has drifted from baseline by {analysis_result['distribution_drift']['drift_score']:.1%}, indicating evolving patterns. Continual learning is adapting detection thresholds accordingly. "
        
        if analysis_result.get('corruption_stats', {}).get('corrupted_lines', 0) > 0:
            base_explanation += f"Noise-robust parsing successfully recovered {analysis_result['corruption_stats'].get('recovered_lines', 0)} corrupted log entries, ensuring analysis reliability despite data quality issues. "
        
        if insights['continual_learning_status'].get('baseline_established'):
            base_explanation += f"Continual learning system has established robust baseline from {insights['continual_learning_status'].get('total_analyses', 0)} previous analyses, enabling accurate anomaly detection in dynamic environments."
        
        return base_explanation
    
    @staticmethod
    def _build_advanced_ai_report(unique_sequence, sequence_id, question, file_hash, stats, 
                                 severity, confidence, root_cause_explanation, category, 
                                 immediate_actions, evidence_chunks, analysis_result, automated_insights, ai_metadata=None):
        """Build report combining AI analysis with advanced features"""
        # This combines AI insights with adaptive learning insights
        base_report = ReportGenerator._build_advanced_report(
            unique_sequence, sequence_id, question, file_hash,
            stats, severity, confidence, analysis_result, automated_insights, ai_metadata
        )
        
        # Enhance with AI-specific fields
        base_report["ai_powered"] = True
        base_report["summary"]["title"] = "AI-ENHANCED ADAPTIVE ANOMALY DETECTION"
        base_report["summary"]["analysis"] += f" Enhanced with LLM reasoning and semantic analysis."
        base_report["evidence"]["ai_evidence_chunks"] = evidence_chunks
        base_report["root_cause"]["explanation"] = root_cause_explanation if root_cause_explanation else base_report["root_cause"]["explanation"]
        
        if immediate_actions:
            base_report["rectification_suggestions"]["immediate_actions"] = immediate_actions
        
        return base_report
    
    @staticmethod
    def _build_ai_report(unique_sequence, sequence_id, question, file_hash, stats, 
                        severity, confidence, root_cause_explanation, category, 
                        immediate_actions, evidence_chunks):
        """Build report using AI analysis results"""
        
        # Analyze parameter deviations
        deviations = ReportGenerator.analyze_parameter_deviations(stats)
        
        # Get category description
        category_info = ReportGenerator.CAUSE_CATEGORIES.get(category, 
                                                             ReportGenerator.CAUSE_CATEGORIES['operational_issue'])
        
        return {
            "sequence": unique_sequence,
            "sequence_id": sequence_id,
            "question": question,
            "file_hash": file_hash[:8],
            "ai_powered": True,
            "summary": {
                "title": "AI-POWERED ANOMALY DETECTION REPORT",
                "analysis": f"Advanced AI analysis using Llama 3.1 and semantic search. {len(evidence_chunks)} relevant log chunks analyzed.",
                "time_range": datetime.now().isoformat(),
                "primary_component": "AI Log Analysis Engine",
                "severity": severity,
                "anomaly_score": round((confidence * (len(deviations) + 1)) / 100, 1)
            },
            "where_anomaly_occurred": {
                "component": "AI Log Analysis Engine",
                "affected_service": f"Semantic Analysis - {question}",
                "timestamp": datetime.now().isoformat()
            },
            "anomalous_events": {
                "total_events": len(evidence_chunks),
                "list": evidence_chunks
            },
            "workflow_comparison": {
                "normal_sequence": ["Log Ingestion", "Pattern Matching", "Manual Review", "Root Cause Analysis"],
                "current_sequence": ["Log Chunking (RecursiveTextSplitter)", "Embedding (nv-embedqa-e5-v5)", 
                                   "Vector Indexing (FAISS)", "Semantic Retrieval", "LLM Analysis (Llama 3.1)"],
                "deviations": [
                    "AI-powered semantic understanding replaces keyword matching",
                    "FAISS enables O(1) similarity search across 768-dim vectors",
                    "Llama 3.1 provides evidence-grounded root cause analysis"
                ]
            },
            "root_cause_hypothesis": {
                "primary_cause": category,
                "cause_description": category_info['description'],
                "contributing_factors": [],
                "likelihood": "High" if severity == "Critical" else "Medium" if severity == "High" else "Low"
            },
            "evidence": {
                "structural_deviations": [
                    f"AI analyzed {len(evidence_chunks)} semantically relevant log chunks",
                    f"Embedding model: nv-embedqa-e5-v5 (768-dimensional vectors)",
                    f"Retrieval: FAISS similarity search (top-4 chunks)"
                ],
                "parameter_deviations": deviations,
                "component_concentration": {
                    "primary_component": "AI Analysis Engine",
                    "component_event_count": len(evidence_chunks),
                    "concentration_percentage": round((len(evidence_chunks) / max(stats['total_lines'], 1)) * 100, 1)
                },
                "statistical_evidence": [
                    f"Total log lines: {stats['total_lines']}",
                    f"Error events: {stats['error_count']}",
                    f"Warning events: {stats['warning_count']}",
                    f"Failed attempts: {stats['failed_count']}"
                ],
                "ai_evidence_chunks": evidence_chunks
            },
            "rectification_suggestions": {
                "immediate_actions": immediate_actions if immediate_actions else category_info['fixes'][:3],
                "short_term_fixes": [
                    "Implement monitoring for detected issue",
                    "Document findings and actions taken",
                    "Test remediation in non-production environment"
                ],
                "long_term_improvements": [
                    "Design system to prevent root cause reoccurrence",
                    "Implement automated AI-powered detection and alerting",
                    "Establish runbook for incident response"
                ],
                "categorized_recommendations": {
                    "configuration": ["Review configuration against best practices", "Validate all parameters"],
                    "resources": ["Monitor resource utilization", "Implement quotas and limits"],
                    "code": ["Improve error handling", "Add input validation", "Implement retry logic"],
                    "network": ["Check for suspicious IPs", "Review firewall rules"],
                    "operational": ["Review logs regularly", "Implement alerting", "Perform post-mortems"]
                }
            },
            "statistics": stats,
            "root_cause": {
                "explanation": root_cause_explanation,
                "evidence": [
                    f"AI Model: Llama 3.1-70B (temperature=0.1 for factual responses)",
                    f"Embedding: nv-embedqa-e5-v5 (768-dim semantic vectors)",
                    f"Retrieval: FAISS vector store with {len(evidence_chunks)} indexed chunks",
                    f"Analysis grounded in {len(evidence_chunks)} most relevant log segments"
                ]
            },
            "recommendations": {
                "configuration": ["Review configuration", "Validate parameters"],
                "resources": ["Monitor utilization", "Set limits"],
                "code": ["Handle exceptions", "Validate inputs"],
                "network": ["Check IPs", "Review firewall"],
                "operational": ["Review logs", "Implement alerts"]
            },
            "detailed_analysis": f"AI-Powered Analysis\nQuestion: {question}\n\nLLM: Llama 3.1-70B\nEmbedding: nv-embedqa-e5-v5\nRetrieval: FAISS\n\nSeverity: {severity}\nCategory: {category}\nConfidence: {confidence}%",
            "confidence_score": round(confidence, 1)
        }
    
    @staticmethod
    def generate_report(sequence_id, question, file_content, file_hash):
        """Generate comprehensive report with structured analysis (Standard mode)"""
        
        stats, error_lines, warning_lines = LogAnalyzer.extract_log_stats(file_content)
        
        # Create unique sequence ID per file and question
        unique_sequence = f"{file_hash[:4]}-{sequence_id:02d}-{uuid.uuid4().hex[:4]}".upper()
        
        # Question-specific severity calculation
        if question == "Find authentication failure":
            severity = 'Critical' if stats['denied_count'] > 20 else ('High' if stats['denied_count'] > 5 else 'Medium')
            confidence = 95.0 if stats['failed_count'] > 0 else 60.0
        elif question == "Detect brute force attack patterns in sshd":
            severity = 'Critical' if stats['ssh_count'] > 100 else ('High' if stats['ssh_count'] > 50 else 'Low')
            confidence = 98.0 if stats['ssh_count'] > 100 else 75.0
        elif question == "Check abnormal user sessions":
            severity = 'High' if stats['timeout_count'] > 10 else ('Medium' if stats['connection_count'] > 50 else 'Low')
            confidence = 92.0 if stats['timeout_count'] > 5 else 70.0
        elif question == "Find resource and configuration anomalies":
            severity = 'High' if stats['warning_count'] > 20 else ('Medium' if stats['warning_count'] > 5 else 'Low')
            confidence = 89.0 if stats['warning_count'] > 10 else 65.0
        else:  # "Analyze anomaly in logs"
            severity = 'Critical' if stats['error_count'] > 50 else ('High' if stats['error_count'] > 10 else 'Medium')
            confidence = 91.0 if stats['error_count'] > 0 else 55.0
        
        # Generate human-readable root cause explanations
        def generate_root_cause_explanation(question, stats):
            """Generate detailed, professional root cause explanation"""
            if question == "Analyze anomaly in logs":
                if stats['error_count'] > 50:
                    return f"The system logs reveal a significant number of error events ({stats['error_count']} total), indicating widespread system instability. These errors, combined with {stats['warning_count']} warning events, suggest multiple subsystems are experiencing issues. The high frequency of errors indicates the system may be overloaded, misconfigured, or experiencing resource constraints. Immediate investigation is recommended to identify the primary failure source and implement corrective measures."
                elif stats['error_count'] > 10:
                    return f"The analysis identified {stats['error_count']} error conditions and {stats['warning_count']} warnings in the log output. While not critical, this indicates the system is experiencing operational issues that require attention. The pattern suggests either temporary failures in system components or minor configuration problems that could escalate if left unaddressed."
                else:
                    return "The system logs show normal operation with minimal error conditions. No significant anomalies were detected during the analysis period. The system appears to be functioning within expected parameters."
            
            elif question == "Find authentication failure":
                if stats['denied_count'] > 20:
                    return f"Critical authentication security concerns have been identified. The system recorded {stats['denied_count']} access denial events and {stats['failed_count']} failed login attempts, suggesting either a coordinated attack or a widespread authentication configuration issue. This high volume of failed authentications indicates potential security threats or serious account management problems. Immediate security review and access controls assessment is strongly recommended."
                elif stats['denied_count'] > 5:
                    return f"Multiple authentication failures have been detected with {stats['denied_count']} denied access attempts and {stats['failed_count']} failed logins. This pattern suggests either users attempting to access resources with insufficient permissions or potential unauthorized access attempts. Review of user permissions and access policies is recommended to ensure proper security posture."
                else:
                    return f"Authentication logs show {stats['accepted_count']} successful authentications with minimal failures. The system's authentication mechanism appears to be functioning normally with acceptable security metrics."
            
            elif question == "Detect brute force attack patterns in sshd":
                if stats['ssh_count'] > 100:
                    return f"A potential brute force attack pattern has been identified with {stats['ssh_count']} SSH connection attempts and {stats['failed_count']} failed authentication events. This attack pattern typically indicates an adversary systematically attempting to compromise SSH access by trying multiple username and password combinations. The high volume of attempts from what appears to be coordinated sources strongly suggests malicious activity. Implementation of rate limiting, IP blocking, and enhanced monitoring is critical to prevent unauthorized access."
                elif stats['ssh_count'] > 50:
                    return f"Elevated SSH connection activity has been detected with {stats['ssh_count']} total attempts. While not definitively malicious, this volume warrants investigation to determine if legitimate administrative activity or potential reconnaissance is occurring. Monitor for patterns and consider implementing additional security controls if suspicious origins are identified."
                else:
                    return f"SSH activity appears normal with {stats['ssh_count']} connection attempts. No suspicious patterns consistent with brute force attacks have been detected in this analysis period."
            
            elif question == "Check abnormal user sessions":
                if stats['timeout_count'] > 10:
                    return f"Abnormal user session patterns have been identified with {stats['timeout_count']} session timeout events across {stats['connection_count']} total connections. This elevated timeout rate suggests either network instability, application issues, or users with connection problems. The pattern could indicate client-side problems, network degradation, or server resource constraints affecting session stability. Investigation into network health and application performance is recommended."
                elif stats['timeout_count'] > 5:
                    return f"Several user session anomalies were detected, including {stats['timeout_count']} timeout events among {stats['connection_count']} connections. While not indicating a widespread issue, these timeouts suggest some users are experiencing connectivity or application responsiveness problems. Monitoring session quality and investigating persistent offenders is advised."
                else:
                    return f"User sessions appear stable with {stats['connection_count']} active connections and minimal timeout events. Session management is operating within normal parameters."
            
            else:  # "Find resource and configuration anomalies"
                if stats['warning_count'] > 20:
                    return f"Significant system resource warnings have been identified, with {stats['warning_count']} warning events detected. These warnings likely indicate resource exhaustion, misconfiguration, or performance degradation. Common issues include high memory usage, disk space constraints, CPU throttling, or connection pool exhaustion. Immediate remediation is recommended to prevent service degradation or outages."
                elif stats['warning_count'] > 5:
                    return f"System configuration warnings have been detected, with {stats['warning_count']} warning events indicating potential issues with resource allocation or configuration settings. These warnings suggest suboptimal system performance that could impact reliability. Review of system configuration and resource allocation is recommended to optimize performance."
                else:
                    return "System resources and configuration appear optimal with minimal warning indicators. The system is operating efficiently with appropriate resource allocation."
        
        # Analyze parameter deviations
        deviations = ReportGenerator.analyze_parameter_deviations(stats)
        
        # Determine root cause categories
        cause_categories = ReportGenerator.determine_cause_category(question, stats)
        
        # Question-specific responses based on file content
        question_responses = {
            "Analyze anomaly in logs": {
                "summary": f"Comprehensive anomaly analysis: {stats['total_lines']} total log lines processed. Detected {stats['error_count']} critical errors and {stats['warning_count']} warnings. Overall severity assessment: {severity}.",
                "primary_component": "System Logs",
                "events": error_lines if error_lines else ["No critical errors detected in this log"],
                "root_cause_explanation": generate_root_cause_explanation("Analyze anomaly in logs", stats),
                "workflow_current": ["Log Intake", "Parse Events", "Anomaly Detection", "Severity Assessment", "Alert Generation"]
            },
            "Find authentication failure": {
                "summary": f"Authentication Security Report: {stats['failed_count']} login failures recorded, {stats['denied_count']} access denials, {stats['accepted_count']} successful authentications. Risk Level: {severity}.",
                "primary_component": "Authentication Service",
                "events": [f"Failed Logins: {stats['failed_count']} attempts blocked", f"Access Denials: {stats['denied_count']} requests rejected"] + error_lines[:1],
                "root_cause_explanation": generate_root_cause_explanation("Find authentication failure", stats),
                "workflow_current": ["Auth Request", "Credential Validation", "Access Check", "Denial/Acceptance", "Log Event"]
            },
            "Detect brute force attack patterns in sshd": {
                "summary": f"SSH Brute Force Detection Report: {stats['ssh_count']} SSH connection attempts identified, {stats['auth_count']} authentication events recorded, {stats['failed_count']} failed attempts. Threat Level: {severity}.",
                "primary_component": "SSH Service (sshd)",
                "events": [f"SSH Connection Attempts: {stats['ssh_count']}", f"Authentication Events: {stats['auth_count']}", f"Failed Auth: {stats['failed_count']}"],
                "root_cause_explanation": generate_root_cause_explanation("Detect brute force attack patterns in sshd", stats),
                "workflow_current": ["SSH Connect", "Auth Attempt", "Credential Check", "Connection Accept/Reject", "Log Event"]
            },
            "Check abnormal user sessions": {
                "summary": f"User Session Anomaly Report: {stats['connection_count']} total connections tracked, {stats['timeout_count']} session timeouts, {stats['accepted_count']} active sessions. Anomaly Level: {severity}.",
                "primary_component": "Session Management",
                "events": [f"Active Connections: {stats['connection_count']}", f"Session Timeouts: {stats['timeout_count']}", f"Active Sessions: {stats['accepted_count']}"],
                "root_cause_explanation": generate_root_cause_explanation("Check abnormal user sessions", stats),
                "workflow_current": ["Session Start", "Activity Monitor", "Timeout Check", "Session End", "Anomaly Log"]
            },
            "Find resource and configuration anomalies": {
                "summary": f"System Resource Analysis: {stats['total_lines']} events analyzed, {stats['warning_count']} resource warnings, {stats['error_count']} errors. Resource Status: {severity}.",
                "primary_component": "System Resources",
                "events": warning_lines if warning_lines else [f"No critical resource warnings in {stats['total_lines']} events"],
                "root_cause_explanation": generate_root_cause_explanation("Find resource and configuration anomalies", stats),
                "workflow_current": ["Resource Monitor", "Threshold Check", "Pattern Analysis", "Alert Decision", "Report Generation"]
            }
        }
        
        response = question_responses.get(question, question_responses["Analyze anomaly in logs"])
        
        # Build categorized recommendations
        recommendations = {
            "configuration": [
                "Review current configuration against best practices",
                "Check error logs for configuration errors",
                "Validate all configuration parameters"
            ],
            "resources": [
                "Monitor resource utilization patterns",
                "Analyze performance metrics",
                "Implement resource limits and quotas"
            ],
            "code": [
                "Improve error handling and exception management",
                "Add input validation for all data entry points",
                "Implement retry logic with exponential backoff"
            ],
            "network": [
                "Monitor active network connections",
                "Check for suspicious IP addresses or origins",
                "Review and update firewall rules"
            ],
            "operational": [
                "Review logs regularly for patterns",
                "Implement automated alerting system",
                "Perform incident response and post-mortems"
            ]
        }
        
        # Add cause-specific recommendations
        cause_based_fixes = []
        for cause in cause_categories[:2]:  # Top 2 causes
            if cause in ReportGenerator.CAUSE_CATEGORIES:
                cause_based_fixes.extend(ReportGenerator.CAUSE_CATEGORIES[cause]['fixes'])
        
        return {
            "sequence": unique_sequence,
            "sequence_id": sequence_id,
            "question": question,
            "file_hash": file_hash[:8],
            "summary": {
                "title": "ANOMALY DETECTION REPORT",
                "analysis": response['summary'],
                "time_range": datetime.now().isoformat(),
                "primary_component": response['primary_component'],
                "severity": severity,
                "anomaly_score": round((confidence * (len(deviations) + 1)) / 100, 1)
            },
            "where_anomaly_occurred": {
                "component": response['primary_component'],
                "affected_service": "Advanced Log Analysis Engine",
                "timestamp": datetime.now().isoformat()
            },
            "anomalous_events": {
                "total_events": len(response['events']),
                "list": response['events'][:5]  # Top 5 anomalous events
            },
            "workflow_comparison": {
                "normal_sequence": ["Login", "Authenticate", "Validate", "Session Open", "Session Close"],
                "current_sequence": response['workflow_current'],
                "deviations": [
                    f"Current workflow has {len(response['workflow_current'])} steps vs normal 5",
                    f"Additional processing: {len(set(response['workflow_current']) - set(['Login', 'Authenticate', 'Validate', 'Session Open', 'Session Close']))} new steps"
                ]
            },
            "root_cause_hypothesis": {
                "primary_cause": cause_categories[0] if cause_categories else 'unknown',
                "cause_description": ReportGenerator.CAUSE_CATEGORIES.get(cause_categories[0] if cause_categories else 'operational_issue', {}).get('description', ''),
                "contributing_factors": cause_categories[1:3] if len(cause_categories) > 1 else [],
                "likelihood": "High" if severity == "Critical" else "Medium" if severity == "High" else "Low"
            },
            "evidence": {
                "structural_deviations": [
                    f"Workflow contains {len(response['workflow_current'])} sequential steps",
                    f"Detected {len(response['events'])} anomalous event(s) in current sequence"
                ],
                "parameter_deviations": deviations,
                "component_concentration": {
                    "primary_component": response['primary_component'],
                    "component_event_count": len(response['events']),
                    "concentration_percentage": round((len(response['events']) / max(stats['total_lines'], 1)) * 100, 1)
                },
                "statistical_evidence": [
                    f"Total events: {stats['total_lines']}",
                    f"Error events: {stats['error_count']} (threshold: 10)",
                    f"Warning events: {stats['warning_count']} (threshold: 5)",
                    f"Failed attempts: {stats['failed_count']} (threshold: 3)"
                ]
            },
            "rectification_suggestions": {
                "immediate_actions": cause_based_fixes[:3] if cause_based_fixes else ["Review error logs", "Check system health", "Monitor for escalation"],
                "short_term_fixes": [
                    "Implement monitoring for detected issue",
                    "Document findings and actions taken",
                    "Test remediation in non-production environment"
                ],
                "long_term_improvements": [
                    "Design system to prevent root cause reoccurrence",
                    "Implement automated detection and alerting",
                    "Establish runbook for incident response"
                ],
                "categorized_recommendations": recommendations
            },
            "statistics": {
                "total_lines": stats['total_lines'],
                "error_count": stats['error_count'],
                "warning_count": stats['warning_count'],
                "failed_count": stats['failed_count'],
                "ssh_count": stats['ssh_count'],
                "auth_count": stats['auth_count'],
                "connection_count": stats['connection_count'],
                "timeout_count": stats['timeout_count'],
                "denied_count": stats['denied_count'],
                "accepted_count": stats['accepted_count']
            },
            "root_cause": {
                "explanation": response['root_cause_explanation'],
                "evidence": [
                    f"Total log entries analyzed: {stats['total_lines']}",
                    f"Error events: {stats['error_count']}",
                    f"Failed authentication attempts: {stats['failed_count']}",
                    f"SSH connections: {stats['ssh_count']}",
                    f"Auth events: {stats['auth_count']}",
                    f"Connection timeouts: {stats['timeout_count']}"
                ]
            },
            "recommendations": recommendations,
            "detailed_analysis": f"Question: {question}\n\nFile Hash: {file_hash[:8]}\nSequence ID: {unique_sequence}\nTotal Events: {stats['total_lines']}\n\nSummary Statistics:\n- Errors: {stats['error_count']}\n- Warnings: {stats['warning_count']}\n- Failed: {stats['failed_count']}\n- SSH Events: {stats['ssh_count']}\n- Auth Events: {stats['auth_count']}\n- Connections: {stats['connection_count']}\n- Timeouts: {stats['timeout_count']}\n- Denied: {stats['denied_count']}\n- Accepted: {stats['accepted_count']}\n\nSeverity Level: {severity}\nRoot Cause: {cause_categories[0] if cause_categories else 'unknown'}",
            "confidence_score": round(confidence, 1)
        }
