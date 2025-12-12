"""
AI-Powered Log Analyzer using NVIDIA AI Models
Uses nv-embedqa-e5-v5 for embeddings, Llama 3.1 for reasoning, and FAISS for retrieval
"""
import os
import hashlib
from typing import List, Dict, Tuple, Optional, Any
import numpy as np

try:
    from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain.schema import Document
    NVIDIA_AVAILABLE = True
except ImportError:
    NVIDIA_AVAILABLE = False
    print("Warning: NVIDIA AI endpoints not available. Install with: pip install langchain-nvidia-ai-endpoints")
    # Create dummy types for type hints
    FAISS = Any
    Document = Any


class AILogAnalyzer:
    """Advanced log analyzer using NVIDIA AI models and FAISS vector search"""
    
    def __init__(self, nvidia_api_key: str = None):
        """Initialize AI analyzer with NVIDIA models"""
        self.nvidia_api_key = nvidia_api_key or os.getenv("NVIDIA_API_KEY")
        
        if not NVIDIA_AVAILABLE:
            raise ImportError("NVIDIA AI endpoints not installed. Run: pip install langchain-nvidia-ai-endpoints langchain-community faiss-cpu")
        
        if not self.nvidia_api_key:
            raise ValueError("NVIDIA_API_KEY not found. Set it in environment or .env file")
        
        # 1. Semantic Embedding Model: nv-embedqa-e5-v5 (768-dimensional vectors)
        self.embeddings = NVIDIAEmbeddings(
            model="nv-embedqa-e5-v5",
            nvidia_api_key=self.nvidia_api_key
        )
        
        # 2. Large Language Model: Llama 3.1 (via ChatNVIDIA)
        # Configured with low temperature (0.1) for factual, evidence-backed responses
        self.llm = ChatNVIDIA(
            model="meta/llama-3.1-70b-instruct",
            nvidia_api_key=self.nvidia_api_key,
            temperature=0.1,  # Low temperature for factual responses
            max_tokens=1024
        )
        
        # 4. Text Processing: RecursiveCharacterTextSplitter
        # Splits logs into manageable chunks with hierarchical separators
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,  # Keep 1-3 related log entries together
            chunk_overlap=50,  # Overlapping boundaries for context preservation
            separators=["\n\n", "\n", " ", ""],  # Hierarchical separators
            length_function=len
        )
        
        self.vector_store = None
        self.log_chunks = []
        self.embedding_time = 0  # Track embedding time
    
    def process_log_file(self, log_content: str) -> Tuple[Dict, Any]:
        """
        Process log file: chunk, embed, and index with FAISS
        
        Returns:
            - statistics dictionary (includes embedding_time_ms)
            - FAISS vector store for retrieval
        """
        import time
        
        # Extract basic statistics first (fallback for compatibility)
        stats = self._extract_basic_stats(log_content)
        
        # Split log content into chunks using RecursiveCharacterTextSplitter
        documents = [Document(page_content=log_content, metadata={"source": "log_file"})]
        self.log_chunks = self.text_splitter.split_documents(documents)
        
        print(f"📝 Split log into {len(self.log_chunks)} chunks")
        
        # 3. Vector Retrieval Model: FAISS
        # Create FAISS index from embeddings for O(1) similarity search
        if self.log_chunks:
            embedding_start = time.time()
            self.vector_store = FAISS.from_documents(
                self.log_chunks,
                self.embeddings
            )
            self.embedding_time = (time.time() - embedding_start) * 1000
            stats['embedding_time_ms'] = self.embedding_time
            print(f"✅ Indexed {len(self.log_chunks)} chunks in FAISS vector store ({self.embedding_time:.2f}ms)")
        
        return stats, self.vector_store
    
    def analyze_with_llm(self, question: str, top_k: int = 4) -> Dict:
        """
        Analyze logs using semantic retrieval + LLM reasoning
        
        Args:
            question: User's analysis question
            top_k: Number of relevant chunks to retrieve (default: 4)
        
        Returns:
            Analysis results with root cause, evidence, recommendations, and timing metadata
        """
        import time
        
        if not self.vector_store:
            raise ValueError("No vector store available. Call process_log_file() first.")
        
        # Track retrieval time
        retrieval_start = time.time()
        relevant_docs = self.vector_store.similarity_search(question, k=top_k)
        retrieval_time = (time.time() - retrieval_start) * 1000
        
        # Combine relevant chunks into context
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Construct prompt for Llama 3.1 with evidence-grounded instructions
        prompt = f"""You are an expert log analyst. Analyze the following log entries and answer the question based ONLY on the evidence provided.

Question: {question}

Log Entries:
{context}

Provide a structured analysis with:
1. **Root Cause**: What is the primary issue? (2-3 sentences)
2. **Evidence**: What specific log entries support this conclusion?
3. **Severity**: Critical, High, Medium, or Low
4. **Category**: security_threat, resource_exhaustion, configuration_error, network_issue, application_error, or operational_issue
5. **Immediate Actions**: 3 specific steps to resolve this issue
6. **Recommendations**: Long-term improvements

Be factual and evidence-based. Do not hallucinate information not present in the logs."""

        # Track LLM generation time
        llm_start = time.time()
        response = self.llm.invoke(prompt)
        llm_time = (time.time() - llm_start) * 1000
        
        # Parse LLM response
        analysis = self._parse_llm_response(response.content, relevant_docs)
        
        # Add timing metadata
        analysis['timing_metadata'] = {
            'retrieval_time_ms': retrieval_time,
            'llm_time_ms': llm_time,
            'total_time_ms': retrieval_time + llm_time
        }
        
        return analysis
    
    def _extract_basic_stats(self, content: str) -> Dict:
        """Extract basic statistics from log content (for compatibility)"""
        lines = content.split('\n')
        
        return {
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
    
    def _parse_llm_response(self, response_text: str, evidence_docs: List[Any]) -> Dict:
        """Parse LLM response into structured format"""
        # Extract sections from response
        lines = response_text.split('\n')
        
        result = {
            'llm_analysis': response_text,
            'root_cause_explanation': '',
            'severity': 'Medium',
            'category': 'operational_issue',
            'immediate_actions': [],
            'recommendations': [],
            'evidence_chunks': [doc.page_content[:200] for doc in evidence_docs],
            'confidence_score': 85.0
        }
        
        # Parse response sections
        current_section = None
        for line in lines:
            line_lower = line.lower().strip()
            
            if 'root cause' in line_lower:
                current_section = 'root_cause'
            elif 'severity' in line_lower:
                current_section = 'severity'
                # Extract severity
                for sev in ['Critical', 'High', 'Medium', 'Low']:
                    if sev.lower() in line_lower:
                        result['severity'] = sev
                        break
            elif 'category' in line_lower:
                current_section = 'category'
                # Extract category
                categories = ['security_threat', 'resource_exhaustion', 'configuration_error', 
                            'network_issue', 'application_error', 'operational_issue']
                for cat in categories:
                    if cat.replace('_', ' ') in line_lower or cat in line_lower:
                        result['category'] = cat
                        break
            elif 'immediate action' in line_lower:
                current_section = 'actions'
            elif 'recommendation' in line_lower:
                current_section = 'recommendations'
            elif line.strip() and current_section:
                # Add content to current section
                if current_section == 'root_cause' and not line.startswith('**'):
                    result['root_cause_explanation'] += line + ' '
                elif current_section == 'actions' and (line.strip().startswith('-') or line.strip().startswith('•') or line.strip()[0].isdigit()):
                    result['immediate_actions'].append(line.strip().lstrip('-•0123456789. '))
                elif current_section == 'recommendations' and (line.strip().startswith('-') or line.strip().startswith('•')):
                    result['recommendations'].append(line.strip().lstrip('-• '))
        
        # Clean up root cause
        result['root_cause_explanation'] = result['root_cause_explanation'].strip()
        if not result['root_cause_explanation']:
            result['root_cause_explanation'] = "Analysis completed. Review evidence chunks for detailed findings."
        
        return result
    
    @staticmethod
    def get_file_hash(content: str) -> str:
        """Generate hash of file content"""
        return hashlib.md5(content.encode()).hexdigest()


# Singleton instance for reuse
_ai_analyzer_instance = None

def get_ai_analyzer() -> AILogAnalyzer:
    """Get or create AI analyzer instance"""
    global _ai_analyzer_instance
    
    if _ai_analyzer_instance is None:
        try:
            _ai_analyzer_instance = AILogAnalyzer()
        except Exception as e:
            print(f"⚠️  Could not initialize AI analyzer: {e}")
            print("Falling back to basic analyzer")
            return None
    
    return _ai_analyzer_instance
