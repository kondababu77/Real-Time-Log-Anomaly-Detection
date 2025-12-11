import React, { useState, useEffect } from 'react';
import { Card, Button, Row, Col, Badge, Accordion, Table } from 'react-bootstrap';
import './ReportDisplay.css';

function ReportDisplay({ report, index, expandAll }) {
  const [expanded, setExpanded] = useState(false);

  // Sync with expandAll prop
  useEffect(() => {
    setExpanded(expandAll);
  }, [expandAll]);

  const getSeverityVariant = (severity) => {
    switch (severity) {
      case 'Critical':
        return 'danger';
      case 'High':
        return 'warning';
      case 'Medium':
        return 'info';
      case 'Low':
        return 'success';
      default:
        return 'secondary';
    }
  };

  const getCauseVariant = (cause) => {
    const causeMap = {
      'security_threat': 'danger',
      'resource_exhaustion': 'warning',
      'configuration_error': 'info',
      'network_issue': 'secondary',
      'application_error': 'warning',
      'operational_issue': 'light'
    };
    return causeMap[cause] || 'secondary';
  };

  return (
    <Card className="report-card shadow-sm">
      <Card.Header className="bg-white border-bottom">
        <div className="d-flex justify-content-between align-items-center">
          <div className="flex-grow-1">
            <h5 className="mb-1" style={{color: '#1a3a52', fontFamily: 'Georgia, serif'}}>{report.question}</h5>
            <small className="text-muted">
              Sequence: <code>{report.sequence}</code> | Sequence ID: <strong>#{report.sequence_id}</strong>
            </small>
          </div>
          <div className="d-flex gap-2">
            <Button
              size="sm"
              onClick={() => setExpanded(!expanded)}
              style={{
                background: expanded ? '#1a3a52' : 'white',
                color: expanded ? 'white' : '#1a3a52',
                border: '1px solid #1a3a52',
                fontFamily: 'Georgia, serif',
                borderRadius: '4px'
              }}
            >
              <i className={`bi bi-${expanded ? 'eye-slash' : 'eye'} me-2`}></i>
              {expanded ? 'Hide Details' : 'View Complete Sequence'}
            </Button>
          </div>
        </div>
      </Card.Header>

      <Card.Body>
        <div className="mb-3">
          <Badge bg={getSeverityVariant(report.summary.severity)} className="me-2 px-3 py-2">
            {report.summary.severity} Severity
          </Badge>
          <div className="mt-3">
            <div className="d-flex justify-content-between align-items-center mb-2">
              <span className="fw-bold" style={{fontFamily: 'Georgia, serif'}}>Confidence Score</span>
              <span className="fw-bold" style={{color: '#1a3a52', fontFamily: 'Georgia, serif'}}>{report.confidence_score}%</span>
            </div>
            <div className="progress" style={{ height: '8px' }}>
              <div
                className="progress-bar"
                style={{background: '#1a3a52'}}
                role="progressbar"
                style={{ width: `${report.confidence_score}%` }}
                aria-valuenow={report.confidence_score}
                aria-valuemin="0"
                aria-valuemax="100"
              />
            </div>
          </div>
        </div>

        {expanded && (
          <div className="expanded-content">
            <hr />

            {/* 1. Summary Section */}
            <div className="section mb-4">
              <h6 className="section-title" style={{color: '#1a3a52', fontFamily: 'Georgia, serif', fontWeight: '600'}}>
                <i className="bi bi-clipboard-data me-2"></i>1. Summary
              </h6>
              <Table bordered size="sm" className="mb-0">
                <tbody>
                  <tr>
                    <td className="fw-bold" style={{width: '30%'}}>Sequence ID</td>
                    <td><code>{report.sequence}</code></td>
                  </tr>
                  <tr>
                    <td className="fw-bold">Time Range</td>
                    <td>{new Date(report.summary.time_range).toLocaleString()}</td>
                  </tr>
                  <tr>
                    <td className="fw-bold">Primary Component</td>
                    <td>{report.summary.primary_component}</td>
                  </tr>
                  <tr>
                    <td className="fw-bold">Anomaly Score</td>
                    <td>
                      <Badge bg={report.summary.anomaly_score > 5 ? 'danger' : report.summary.anomaly_score > 2 ? 'warning' : 'success'}>
                        {report.summary.anomaly_score}
                      </Badge>
                    </td>
                  </tr>
                  <tr>
                    <td className="fw-bold">Severity</td>
                    <td><Badge bg={getSeverityVariant(report.summary.severity)}>{report.summary.severity}</Badge></td>
                  </tr>
                </tbody>
              </Table>
              <div className="mt-3 p-3 bg-light rounded">
                <strong>Analysis:</strong> {report.summary.analysis}
              </div>
            </div>

            {/* 2. Where Anomaly Occurred */}
            <div className="section mb-4">
              <h6 className="section-title" style={{color: '#1a3a52', fontFamily: 'Georgia, serif', fontWeight: '600'}}>
                <i className="bi bi-geo-alt me-2"></i>2. Where Anomaly Occurred
              </h6>
              <div className="p-3 border rounded bg-white">
                <Row>
                  <Col md={4}>
                    <strong style={{fontFamily: 'Georgia, serif'}}>Component:</strong><br/>
                    <span style={{color: '#1a3a52', fontFamily: 'Georgia, serif'}}>{report.where_anomaly_occurred?.component || report.summary.primary_component}</span>
                  </Col>
                  <Col md={4}>
                    <strong>Service:</strong><br/>
                    <span>{report.where_anomaly_occurred?.affected_service || 'Log Analysis Service'}</span>
                  </Col>
                  <Col md={4}>
                    <strong>Timestamp:</strong><br/>
                    <span className="text-muted">{new Date(report.where_anomaly_occurred?.timestamp || report.summary.time_range).toLocaleTimeString()}</span>
                  </Col>
                </Row>
              </div>
            </div>

            {/* 3. Anomalous Events List */}
            <div className="section mb-4">
              <h6 className="section-title" style={{color: '#1a3a52', fontFamily: 'Georgia, serif', fontWeight: '600'}}>
                <i className="bi bi-exclamation-triangle me-2"></i>3. Anomalous Events List
              </h6>
              <div className="p-3 border rounded bg-light">
                <div className="mb-2">
                  <Badge bg="secondary">Total Events: {report.anomalous_events?.total_events || report.events?.length || 0}</Badge>
                </div>
                <div className="events-list">
                  {(report.anomalous_events?.list || report.events || []).map((event, i) => (
                    <div key={i} className="event-item p-2 mb-2 bg-white border-start border-danger border-3">
                      <strong className="text-danger">Event #{i + 1}:</strong> {typeof event === 'string' ? event : event.text || JSON.stringify(event)}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* 4. Workflow Comparison */}
            <div className="section mb-4">
              <h6 className="section-title" style={{color: '#1a3a52', fontFamily: 'Georgia, serif', fontWeight: '600'}}>
                <i className="bi bi-diagram-3 me-2"></i>4. Workflow Comparison
              </h6>
              <Row>
                <Col md={6}>
                  <div className="p-3 border rounded bg-success bg-opacity-10">
                    <h6 className="text-success mb-3">
                      <i className="bi bi-check-circle me-2"></i>Normal Workflow
                    </h6>
                    <ol className="mb-0">
                      {(report.workflow_comparison?.normal_sequence || ['Login', 'Authenticate', 'Validate', 'Session Open', 'Session Close']).map((step, i) => (
                        <li key={i} className="mb-2">{step}</li>
                      ))}
                    </ol>
                  </div>
                </Col>
                <Col md={6}>
                  <div className="p-3 border rounded bg-warning bg-opacity-10">
                    <h6 className="text-warning mb-3">
                      <i className="bi bi-arrow-repeat me-2"></i>Current Workflow
                    </h6>
                    <ol className="mb-0">
                      {(report.workflow_comparison?.current_sequence || []).map((step, i) => (
                        <li key={i} className="mb-2">{step}</li>
                      ))}
                    </ol>
                  </div>
                </Col>
              </Row>
              <div className="mt-3 p-3 bg-danger bg-opacity-10 rounded">
                <h6 className="text-danger mb-2">
                  <i className="bi bi-x-circle me-2"></i>Workflow Deviations
                </h6>
                <ul className="mb-0">
                  {(report.workflow_comparison?.deviations || []).map((dev, i) => (
                    <li key={i}>{dev}</li>
                  ))}
                </ul>
              </div>
            </div>

            {/* 5. Root Cause Hypothesis */}
            <div className="section mb-4">
              <h6 className="section-title" style={{color: '#1a3a52', fontFamily: 'Georgia, serif', fontWeight: '600'}}>
                <i className="bi bi-lightbulb me-2"></i>5. Root Cause Hypothesis
              </h6>
              <div className="p-3 border rounded">
                <Table bordered size="sm" className="mb-3">
                  <tbody>
                    <tr>
                      <td className="fw-bold" style={{width: '30%'}}>Primary Cause</td>
                      <td>
                        <Badge bg={getCauseVariant(report.root_cause_hypothesis?.primary_cause)}>
                          {(report.root_cause_hypothesis?.primary_cause || 'unknown').replace(/_/g, ' ').toUpperCase()}
                        </Badge>
                      </td>
                    </tr>
                    <tr>
                      <td className="fw-bold">Description</td>
                      <td>{report.root_cause_hypothesis?.cause_description}</td>
                    </tr>
                    <tr>
                      <td className="fw-bold">Likelihood</td>
                      <td>
                        <Badge bg={report.root_cause_hypothesis?.likelihood === 'High' ? 'danger' : report.root_cause_hypothesis?.likelihood === 'Medium' ? 'warning' : 'info'}>
                          {report.root_cause_hypothesis?.likelihood}
                        </Badge>
                      </td>
                    </tr>
                    {report.root_cause_hypothesis?.contributing_factors?.length > 0 && (
                      <tr>
                        <td className="fw-bold">Contributing Factors</td>
                        <td>
                          {report.root_cause_hypothesis.contributing_factors.map((factor, i) => (
                            <Badge key={i} bg="secondary" className="me-2">
                              {factor.replace(/_/g, ' ')}
                            </Badge>
                          ))}
                        </td>
                      </tr>
                    )}
                  </tbody>
                </Table>
                <div className="p-3 bg-light rounded">
                  <strong>Detailed Explanation:</strong>
                  <p className="mb-0 mt-2">{report.root_cause.explanation}</p>
                </div>
              </div>
            </div>

            {/* 6. Evidence Section */}
            <div className="section mb-4">
              <h6 className="section-title" style={{color: '#1a3a52', fontFamily: 'Georgia, serif', fontWeight: '600'}}>
                <i className="bi bi-file-earmark-text me-2"></i>6. Evidence
              </h6>
              
              {/* Structural Deviations */}
              <div className="mb-3">
                <h6 className="fw-bold" style={{color: '#1a3a52', fontFamily: 'Georgia, serif'}}>Structural Deviations</h6>
                <ul className="list-unstyled">
                  {(report.evidence?.structural_deviations || []).map((item, i) => (
                    <li key={i} className="mb-2">
                      <i className="bi bi-arrow-right-circle me-2" style={{color: '#1a3a52'}}></i>{item}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Parameter Deviations */}
              {report.evidence?.parameter_deviations?.length > 0 && (
                <div className="mb-3">
                  <h6 className="fw-bold text-danger">Parameter Deviations (Out-of-Range)</h6>
                  <Table striped bordered hover size="sm">
                    <thead className="table-danger">
                      <tr>
                        <th>Parameter</th>
                        <th>Current Value</th>
                        <th>Normal Threshold</th>
                        <th>Deviation</th>
                        <th>Severity</th>
                      </tr>
                    </thead>
                    <tbody>
                      {report.evidence.parameter_deviations.map((dev, i) => (
                        <tr key={i}>
                          <td className="fw-bold">{dev.parameter.replace(/_/g, ' ')}</td>
                          <td><Badge bg="danger">{dev.value}</Badge></td>
                          <td>{dev.normal_threshold}</td>
                          <td>
                            <Badge bg="warning">
                              {dev.deviation_type} (+{dev.deviation_percent}%)
                            </Badge>
                          </td>
                          <td>
                            <Badge bg={dev.deviation_percent > 100 ? 'danger' : 'warning'}>
                              {dev.deviation_percent > 100 ? 'Critical' : 'High'}
                            </Badge>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                </div>
              )}

              {/* Component Concentration */}
              <div className="mb-3">
                <h6 className="fw-bold" style={{color: '#1565c0', fontFamily: 'Georgia, serif'}}>Component Concentration</h6>
                <div className="p-3 bg-info bg-opacity-10 rounded">
                  <Row>
                    <Col md={4}>
                      <strong style={{fontFamily: 'Georgia, serif'}}>Primary Component:</strong><br/>
                      {report.evidence?.component_concentration?.primary_component}
                    </Col>
                    <Col md={4}>
                      <strong style={{fontFamily: 'Georgia, serif'}}>Event Count:</strong><br/>
                      <Badge bg="info">{report.evidence?.component_concentration?.component_event_count}</Badge>
                    </Col>
                    <Col md={4}>
                      <strong>Concentration:</strong><br/>
                      <Badge bg="info">{report.evidence?.component_concentration?.concentration_percentage}%</Badge>
                    </Col>
                  </Row>
                </div>
              </div>

              {/* Statistical Evidence */}
              <div className="mb-3">
                <h6 className="fw-bold text-secondary">Statistical Evidence</h6>
                <ul className="list-unstyled">
                  {(report.evidence?.statistical_evidence || report.root_cause?.evidence || []).map((item, i) => (
                    <li key={i} className="mb-2">
                      <i className="bi bi-graph-up text-secondary me-2"></i>{item}
                    </li>
                  ))}
                </ul>
              </div>

              {/* AI Evidence Chunks (if available) */}
              {report.evidence?.ai_evidence_chunks?.length > 0 && (
                <div className="mb-3">
                  <h6 className="fw-bold text-success">
                    <i className="bi bi-robot me-2"></i>AI Evidence Chunks
                  </h6>
                  <Accordion>
                    {report.evidence.ai_evidence_chunks.map((chunk, i) => (
                      <Accordion.Item key={i} eventKey={i.toString()}>
                        <Accordion.Header>Evidence Chunk #{i + 1}</Accordion.Header>
                        <Accordion.Body>
                          <pre className="bg-light p-3 rounded" style={{fontSize: '0.85rem'}}>
                            {typeof chunk === 'string' ? chunk : JSON.stringify(chunk, null, 2)}
                          </pre>
                        </Accordion.Body>
                      </Accordion.Item>
                    ))}
                  </Accordion>
                </div>
              )}
            </div>

            {/* 7. Rectification Suggestions */}
            <div className="section mb-4">
              <h6 className="section-title" style={{color: '#1a3a52', fontFamily: 'Georgia, serif', fontWeight: '600'}}>
                <i className="bi bi-tools me-2"></i>7. Rectification Suggestions
              </h6>
              
              {/* Immediate Actions */}
              <div className="mb-3">
                <h6 className="fw-bold text-danger">
                  <i className="bi bi-lightning me-2"></i>Immediate Actions (Do Now)
                </h6>
                <ul className="list-group">
                  {(report.rectification_suggestions?.immediate_actions || []).map((action, i) => (
                    <li key={i} className="list-group-item list-group-item-danger">
                      <i className="bi bi-exclamation-circle me-2"></i>{action}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Short-Term Fixes */}
              <div className="mb-3">
                <h6 className="fw-bold text-warning">
                  <i className="bi bi-calendar-week me-2"></i>Short-Term Fixes (Next Few Days)
                </h6>
                <ul className="list-group">
                  {(report.rectification_suggestions?.short_term_fixes || []).map((fix, i) => (
                    <li key={i} className="list-group-item list-group-item-warning">
                      <i className="bi bi-wrench me-2"></i>{fix}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Long-Term Improvements */}
              <div className="mb-3">
                <h6 className="fw-bold text-success">
                  <i className="bi bi-graph-up-arrow me-2"></i>Long-Term Improvements (Strategic)
                </h6>
                <ul className="list-group">
                  {(report.rectification_suggestions?.long_term_improvements || []).map((improvement, i) => (
                    <li key={i} className="list-group-item list-group-item-success">
                      <i className="bi bi-star me-2"></i>{improvement}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Categorized Recommendations */}
              <div className="mt-4">
                <h6 className="fw-bold text-info mb-3">
                  <i className="bi bi-tags me-2"></i>Categorized Recommendations by Type
                </h6>
                <Row>
                  {Object.entries(report.rectification_suggestions?.categorized_recommendations || report.recommendations || {}).map(([category, items]) => (
                    <Col md={6} lg={4} key={category} className="mb-3">
                      <Card className="h-100 border-info">
                        <Card.Header className="bg-info text-white">
                          <i className={`bi bi-${
                            category === 'configuration' ? 'gear' :
                            category === 'resources' ? 'hdd' :
                            category === 'code' ? 'code-slash' :
                            category === 'network' ? 'wifi' :
                            'clipboard-check'
                          } me-2`}></i>
                          {category.charAt(0).toUpperCase() + category.slice(1)}
                        </Card.Header>
                        <Card.Body>
                          <ul className="list-unstyled mb-0" style={{fontSize: '0.9rem'}}>
                            {items.map((item, i) => (
                              <li key={i} className="mb-2">
                                <i className="bi bi-check2 text-success me-2"></i>{item}
                              </li>
                            ))}
                          </ul>
                        </Card.Body>
                      </Card>
                    </Col>
                  ))}
                </Row>
              </div>
            </div>

            {/* 8. Key Statistics */}
            <div className="section mb-4">
              <h6 className="section-title" style={{color: '#1a3a52', fontFamily: 'Georgia, serif', fontWeight: '600'}}>
                <i className="bi bi-bar-chart me-2"></i>8. Key Statistics
              </h6>
              <Row className="g-3">
                {[
                  { label: 'Total Lines', value: report.statistics.total_lines, icon: 'file-text' },
                  { label: 'Errors', value: report.statistics.error_count, icon: 'x-circle', color: 'danger' },
                  { label: 'Warnings', value: report.statistics.warning_count, icon: 'exclamation-triangle', color: 'warning' },
                  { label: 'Failed', value: report.statistics.failed_count, icon: 'x-square', color: 'danger' },
                  { label: 'SSH Events', value: report.statistics.ssh_count, icon: 'terminal' },
                  { label: 'Auth Events', value: report.statistics.auth_count, icon: 'shield-lock' },
                  { label: 'Connections', value: report.statistics.connection_count, icon: 'plug' },
                  { label: 'Timeouts', value: report.statistics.timeout_count, icon: 'clock', color: 'warning' },
                  { label: 'Denied', value: report.statistics.denied_count, icon: 'shield-x', color: 'danger' },
                  { label: 'Accepted', value: report.statistics.accepted_count, icon: 'shield-check', color: 'success' },
                ].map((stat, i) => (
                  <Col md={6} lg={4} xl={3} key={i}>
                    <div className={`stat-box border-${stat.color || 'primary'}`}>
                      <i className={`bi bi-${stat.icon} text-${stat.color || 'primary'}`}></i>
                      <div className="stat-label">{stat.label}</div>
                      <div className={`stat-value text-${stat.color || 'primary'}`}>{stat.value}</div>
                    </div>
                  </Col>
                ))}
              </Row>
            </div>
          </div>
        )}
      </Card.Body>
    </Card>
  );
}

export default ReportDisplay;
