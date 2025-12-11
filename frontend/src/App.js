import React, { useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import FileUploadForm from './components/FileUploadForm';
import ReportDisplay from './components/ReportDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import './App.css';

function App() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [fileName, setFileName] = useState('');
  const [expandAll, setExpandAll] = useState(false);

  const handleFileUpload = async (formData) => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      
      if (data.success) {
        setReports(data.reports);
        setFileName(data.filename);
      } else {
        setError(data.error || 'Failed to analyze file');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleTextAnalysis = async (text) => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('/api/analyze-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ logText: text }),
      });
      const data = await response.json();
      
      if (data.success) {
        setReports(data.reports);
        setFileName('text-input');
      } else {
        setError(data.error || 'Failed to analyze text');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Hero Section - Project Overview */}
      <section className="hero-section py-5 text-white" style={{background: 'linear-gradient(135deg, #1a3a52 0%, #2c5f7c 100%)'}}>
        <Container>
          <Row className="align-items-center py-5">
            <Col lg={12}>
              <div className="text-center">
                <div className="mb-4">
                  <i className="bi bi-shield-check" style={{
                    fontSize: '4rem',
                    display: 'inline-block'
                  }}></i>
                </div>
                <h1 className="display-3 fw-bold mb-4">
                  Advanced Log Anomaly Detection System
                </h1>
                <p className="lead mb-4" style={{fontSize: '1.15rem', lineHeight: '1.7'}}>
                  Research-based log analysis implementing <strong>adaptive hyperparameter optimization</strong>, 
                  {' '}<strong>real-time continual learning</strong>, and{' '}
                  <strong>robust handling of noisy logs</strong>
                </p>
                <Row className="mt-5">
                  <Col md={3} className="mb-3">
                    <div className="feature-box p-4 bg-white bg-opacity-10 rounded">
                      <i className="bi bi-sliders" style={{fontSize: '2.5rem', marginBottom: '1rem'}}></i>
                      <h5 className="fw-bold">Adaptive Optimization</h5>
                      <p className="small mb-0">Auto-tuning thresholds for maximum accuracy</p>
                    </div>
                  </Col>
                  <Col md={3} className="mb-3">
                    <div className="feature-box p-4 bg-white bg-opacity-10 rounded">
                      <i className="bi bi-arrow-repeat" style={{fontSize: '2.5rem', marginBottom: '1rem'}}></i>
                      <h5 className="fw-bold">Continual Learning</h5>
                      <p className="small mb-0">Adapts to evolving log patterns in real-time</p>
                    </div>
                  </Col>
                  <Col md={3} className="mb-3">
                    <div className="feature-box p-4 bg-white bg-opacity-10 rounded">
                      <i className="bi bi-shield-fill-check" style={{fontSize: '2.5rem', marginBottom: '1rem'}}></i>
                      <h5 className="fw-bold">Noise Robust</h5>
                      <p className="small mb-0">Handles corrupted & incomplete log data</p>
                    </div>
                  </Col>
                  <Col md={3} className="mb-3">
                    <div className="feature-box p-4 bg-white bg-opacity-10 rounded">
                      <i className="bi bi-lightbulb" style={{fontSize: '2.5rem', marginBottom: '1rem'}}></i>
                      <h5 className="fw-bold">Auto Insights</h5>
                      <p className="small mb-0">Automated intelligence from detection results</p>
                    </div>
                  </Col>
                </Row>
                <div className="mt-5">
                  <a href="#upload-section" className="btn btn-light btn-lg px-5">
                    <i className="bi bi-arrow-down-circle me-2"></i>
                    Start Analyzing
                  </a>
                </div>
              </div>
            </Col>
          </Row>
        </Container>
      </section>

      {/* Upload/Analysis Section */}
      <section id="upload-section" className="action-section py-5 bg-light">
        <Container>
          <Row className="mb-5">
            <Col lg={12} className="text-center">
              <i className="bi bi-upload display-4 mb-3" style={{color: '#1a3a52'}}></i>
              <h2 className="h1 fw-bold mb-3" style={{color: '#1a3a52'}}>
                Upload & Analyze Your Logs
              </h2>
              <p className="lead text-muted" style={{fontSize: '1.05rem'}}>
                Choose between file upload or direct text input for instant AI-powered analysis
              </p>
            </Col>
          </Row>
          
          <Row className="justify-content-center">
            <Col lg={10} xl={8}>
              <div style={{
                background: '#ffffff',
                borderRadius: '8px',
                padding: '30px',
                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                border: '1px solid #e0e0e0'
              }}>
                <FileUploadForm onFileUpload={handleFileUpload} onTextAnalysis={handleTextAnalysis} />
              </div>
            </Col>
          </Row>

          {error && (
            <Row className="mt-4">
              <Col lg={10} xl={8} className="mx-auto">
                <div className="alert alert-danger alert-dismissible fade show" role="alert">
                  <i className="bi bi-exclamation-triangle-fill me-2"></i>
                  <strong>Error:</strong> {error}
                  <button type="button" className="btn-close" onClick={() => setError('')}></button>
                </div>
              </Col>
            </Row>
          )}

          {loading && <LoadingSpinner />}
        </Container>
      </section>

      {/* How to Use Section */}
      {!loading && reports.length === 0 && !error && (
        <section className="how-to-use-section py-5 bg-white">
          <Container>
            <Row className="mb-5">
              <Col lg={12} className="text-center">
                <i className="bi bi-book display-4 mb-3" style={{color: '#1a3a52'}}></i>
                <h2 className="h1 fw-bold mb-3" style={{color: '#1a3a52'}}>
                  How to Use This System
                </h2>
                <p className="lead text-muted">Follow these simple steps to analyze your logs</p>
              </Col>
            </Row>

            <Row className="g-4 mb-5">
              <Col md={6} lg={3}>
                <div className="step-card text-center p-4 h-100">
                  <div className="step-number mx-auto mb-3">
                    1
                  </div>
                  <h5 className="fw-bold mb-3">Upload or Paste</h5>
                  <p className="text-muted">
                    Upload a log file (.log, .txt) or paste log content directly into the text area above
                  </p>
                </div>
              </Col>
              <Col md={6} lg={3}>
                <div className="step-card text-center p-4 h-100">
                  <div className="step-number mx-auto mb-3" style={{
                    background: '#2e7d32'
                  }}>
                    2
                  </div>
                  <h5 className="fw-bold mb-3">Select Analysis Type</h5>
                  <p className="text-muted">
                    Choose from 5 analysis perspectives: anomalies, auth failures, brute force, sessions, resources
                  </p>
                </div>
              </Col>
              <Col md={6} lg={3}>
                <div className="step-card text-center p-4 h-100">
                  <div className="step-number mx-auto mb-3" style={{
                    background: '#c77700'
                  }}>
                    3
                  </div>
                  <h5 className="fw-bold mb-3">AI Processing</h5>
                  <p className="text-muted">
                    Advanced algorithms process your logs with adaptive optimization and noise handling
                  </p>
                </div>
              </Col>
              <Col md={6} lg={3}>
                <div className="step-card text-center p-4 h-100">
                  <div className="step-number mx-auto mb-3" style={{
                    background: '#1565c0'
                  }}>
                    4
                  </div>
                  <h5 className="fw-bold mb-3">Get Insights</h5>
                  <p className="text-muted">
                    Receive comprehensive reports with automated insights and actionable recommendations
                  </p>
                </div>
              </Col>
            </Row>

            {/* Advanced Features */}
            <Row className="mb-5">
              <Col lg={12}>
                <div className="p-5 rounded" style={{
                  background: '#f5f5f5',
                  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                  border: '1px solid #e0e0e0'
                }}>
                  <h3 className="h2 fw-bold mb-4 text-center" style={{color: '#1a3a52'}}>
                    <i className="bi bi-stars me-2"></i>
                    Advanced Features
                  </h3>
                  <Row className="g-4">
                    <Col md={6}>
                      <div className="d-flex align-items-start p-3 rounded" style={{
                        background: '#ffffff',
                        border: '1px solid #e0e0e0',
                        transition: 'all 0.3s ease'
                      }} onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'translateY(-3px)';
                        e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
                      }} onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'translateY(0)';
                        e.currentTarget.style.boxShadow = 'none';
                      }}>
                        <div className="flex-shrink-0">
                          <i className="bi bi-cpu display-6 me-3" style={{color: '#1a3a52'}}></i>
                        </div>
                        <div>
                          <h5 className="fw-bold">AI Models Integration</h5>
                          <ul className="text-muted">
                            <li><strong>Llama 3.1-70B:</strong> LLM reasoning for root cause analysis</li>
                            <li><strong>nv-embedqa-e5-v5:</strong> 768-dim semantic embeddings</li>
                            <li><strong>FAISS:</strong> O(1) vector similarity search</li>
                          </ul>
                        </div>
                      </div>
                    </Col>
                    <Col md={6}>
                      <div className="d-flex align-items-start p-3 rounded" style={{
                        background: '#ffffff',
                        border: '1px solid #e0e0e0',
                        transition: 'all 0.3s ease'
                      }} onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'translateY(-3px)';
                        e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
                      }} onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'translateY(0)';
                        e.currentTarget.style.boxShadow = 'none';
                      }}>
                        <div className="flex-shrink-0">
                          <i className="bi bi-graph-up display-6 me-3" style={{color: '#2e7d32'}}></i>
                        </div>
                        <div>
                          <h5 className="fw-bold">Adaptive Optimization</h5>
                          <ul className="text-muted">
                            <li>Auto-tuning detection thresholds</li>
                            <li>Dynamic learning rate adjustment</li>
                            <li>Reduces false positives by 30-50%</li>
                          </ul>
                        </div>
                      </div>
                    </Col>
                    <Col md={6}>
                      <div className="d-flex align-items-start p-3 rounded" style={{
                        background: '#ffffff',
                        border: '1px solid #e0e0e0',
                        transition: 'all 0.3s ease'
                      }} onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'translateY(-3px)';
                        e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
                      }} onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'translateY(0)';
                        e.currentTarget.style.boxShadow = 'none';
                      }}>
                        <div className="flex-shrink-0">
                          <i className="bi bi-arrow-clockwise display-6 me-3" style={{color: '#c77700'}}></i>
                        </div>
                        <div>
                          <h5 className="fw-bold">Continual Learning</h5>
                          <ul className="text-muted">
                            <li>Real-time baseline updates</li>
                            <li>Pattern memory without forgetting</li>
                            <li>Distribution drift detection</li>
                          </ul>
                        </div>
                      </div>
                    </Col>
                    <Col md={6}>
                      <div className="d-flex align-items-start p-3 rounded" style={{
                        background: '#ffffff',
                        border: '1px solid #e0e0e0',
                        transition: 'all 0.3s ease'
                      }} onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'translateY(-3px)';
                        e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
                      }} onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'translateY(0)';
                        e.currentTarget.style.boxShadow = 'none';
                      }}>
                        <div className="flex-shrink-0">
                          <i className="bi bi-shield-check display-6 me-3" style={{color: '#1565c0'}}></i>
                        </div>
                        <div>
                          <h5 className="fw-bold">Noise Robustness</h5>
                          <ul className="text-muted">
                            <li>Handles corrupted log entries</li>
                            <li>Multi-encoding support</li>
                            <li>80%+ recovery rate</li>
                          </ul>
                        </div>
                      </div>
                    </Col>
                  </Row>
                </div>
              </Col>
            </Row>

            {/* Analysis Types */}
            <Row>
              <Col lg={12}>
                <h3 className="h2 fw-bold mb-4 text-center" style={{color: '#1a3a52'}}>
                  <i className="bi bi-search me-2"></i>
                  Available Analysis Types
                </h3>
                <Row className="g-3">
                  <Col md={6} lg={4}>
                    <div className="p-4 h-100 rounded" style={{
                      borderLeft: '4px solid #1a3a52',
                      background: '#ffffff',
                      border: '1px solid #e0e0e0',
                      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                      transition: 'all 0.3s ease'
                    }} onMouseEnter={(e) => {
                      e.currentTarget.style.transform = 'translateX(8px)';
                      e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
                    }} onMouseLeave={(e) => {
                      e.currentTarget.style.transform = 'translateX(0)';
                      e.currentTarget.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
                    }}>
                      <h6 className="fw-bold" style={{color: '#1a3a52'}}>
                        <i className="bi bi-bug me-2"></i>General Anomaly Detection
                      </h6>
                      <p className="text-muted small mb-0">
                        Identifies errors, warnings, and unusual patterns in system logs
                      </p>
                    </div>
                  </Col>
                  <Col md={6} lg={4}>
                    <div className="p-4 h-100 rounded" style={{
                      borderLeft: '4px solid #c62828',
                      background: '#ffffff',
                      border: '1px solid #e0e0e0',
                      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                      transition: 'all 0.3s ease'
                    }} onMouseEnter={(e) => {
                      e.currentTarget.style.transform = 'translateX(8px)';
                      e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
                    }} onMouseLeave={(e) => {
                      e.currentTarget.style.transform = 'translateX(0)';
                      e.currentTarget.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
                    }}>
                      <h6 className="fw-bold" style={{color: '#c62828'}}>
                        <i className="bi bi-key me-2"></i>Authentication Failures
                      </h6>
                      <p className="text-muted small mb-0">
                        Detects failed login attempts and access denials
                      </p>
                    </div>
                  </Col>
                  <Col md={6} lg={4}>
                    <div className="p-4 h-100 rounded" style={{
                      borderLeft: '4px solid #c77700',
                      background: '#ffffff',
                      border: '1px solid #e0e0e0',
                      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                      transition: 'all 0.3s ease'
                    }} onMouseEnter={(e) => {
                      e.currentTarget.style.transform = 'translateX(8px)';
                      e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
                    }} onMouseLeave={(e) => {
                      e.currentTarget.style.transform = 'translateX(0)';
                      e.currentTarget.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
                    }}>
                      <h6 className="fw-bold" style={{color: '#c77700'}}>
                        <i className="bi bi-shield-exclamation me-2"></i>Brute Force Attacks
                      </h6>
                      <p className="text-muted small mb-0">
                        Identifies SSH brute force and password attack patterns
                      </p>
                    </div>
                  </Col>
                  <Col md={6} lg={4}>
                    <div className="p-4 h-100 rounded" style={{
                      borderLeft: '4px solid #1565c0',
                      background: '#ffffff',
                      border: '1px solid #e0e0e0',
                      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                      transition: 'all 0.3s ease'
                    }} onMouseEnter={(e) => {
                      e.currentTarget.style.transform = 'translateX(8px)';
                      e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
                    }} onMouseLeave={(e) => {
                      e.currentTarget.style.transform = 'translateX(0)';
                      e.currentTarget.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
                    }}>
                      <h6 className="fw-bold" style={{color: '#1565c0'}}>
                        <i className="bi bi-person-badge me-2"></i>User Session Anomalies
                      </h6>
                      <p className="text-muted small mb-0">
                        Analyzes session timeouts and abnormal user behavior
                      </p>
                    </div>
                  </Col>
                  <Col md={6} lg={4}>
                    <div className="p-4 h-100 rounded" style={{
                      borderLeft: '4px solid #2e7d32',
                      background: '#ffffff',
                      border: '1px solid #e0e0e0',
                      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                      transition: 'all 0.3s ease'
                    }} onMouseEnter={(e) => {
                      e.currentTarget.style.transform = 'translateX(8px)';
                      e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
                    }} onMouseLeave={(e) => {
                      e.currentTarget.style.transform = 'translateX(0)';
                      e.currentTarget.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
                    }}>
                      <h6 className="fw-bold" style={{color: '#2e7d32'}}>
                        <i className="bi bi-hdd me-2"></i>Resource & Config Anomalies
                      </h6>
                      <p className="text-muted small mb-0">
                        Detects resource exhaustion and configuration issues
                      </p>
                    </div>
                  </Col>
                  <Col md={6} lg={4}>
                    <div className="p-4 h-100 rounded" style={{
                      borderLeft: '4px solid #2c5f7c',
                      background: '#ffffff',
                      border: '1px solid #e0e0e0',
                      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                      transition: 'all 0.3s ease'
                    }} onMouseEnter={(e) => {
                      e.currentTarget.style.transform = 'translateX(8px)';
                      e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
                    }} onMouseLeave={(e) => {
                      e.currentTarget.style.transform = 'translateX(0)';
                      e.currentTarget.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
                    }}>
                      <h6 className="fw-bold" style={{color: '#2c5f7c'}}>
                        <i className="bi bi-file-earmark-text me-2"></i>Comprehensive Reports
                      </h6>
                      <p className="text-muted small mb-0">
                        8-section detailed reports with automated insights
                      </p>
                    </div>
                  </Col>
                </Row>
              </Col>
            </Row>
          </Container>
        </section>
      )}

      {/* Reports Section */}
      {reports.length > 0 && !loading && (
        <section className="reports-section py-5 bg-white">
          <Container>
            <Row className="mb-4">
              <Col lg={8}>
                <h2 className="h1 fw-bold mb-2" style={{color: '#1a3a52'}}>
                  <i className="bi bi-clipboard-data me-2"></i>
                  Analysis Report Results
                </h2>
                <p className="text-muted" style={{fontSize: '1.05rem'}}>
                  <i className="bi bi-file-earmark me-1"></i> File: <strong style={{color: '#1a3a52'}}>{fileName}</strong> | 
                  <i className="bi bi-collection me-1"></i> Total Sequences: <strong style={{color: '#2e7d32'}}>{reports.length}</strong>
                </p>
              </Col>
              <Col lg={4} className="text-end">
                <button 
                  className="btn btn-lg px-5"
                  style={{
                    background: '#1a3a52',
                    color: 'white',
                    border: 'none',
                    fontWeight: '600',
                    borderRadius: '4px',
                    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)',
                    transition: 'all 0.3s ease'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-2px)';
                    e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.2)';
                    e.currentTarget.style.background = '#0f2537';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.15)';
                    e.currentTarget.style.background = '#1a3a52';
                  }}
                  onClick={() => setExpandAll(!expandAll)}
                >
                  <i className={`bi bi-${expandAll ? 'arrows-collapse' : 'arrows-expand'} me-2`}></i>
                  {expandAll ? 'Collapse All' : 'Expand All Sequences'}
                </button>
              </Col>
            </Row>
            <Row className="g-4">
              {reports.map((report, index) => (
                <Col lg={12} key={index}>
                  <ReportDisplay report={report} index={index} expandAll={expandAll} />
                </Col>
              ))}
            </Row>
          </Container>
        </section>
      )}

      {/* Footer */}
      <footer className="footer text-white text-center py-4" style={{background: '#1a3a52', fontFamily: 'Georgia, serif'}}>
        <Container>
          <p className="mb-0">&copy; 2024 Anomaly Report Analyzer. Advanced Anomaly Detection System.</p>
        </Container>
      </footer>
    </div>
  );
}

export default App;
