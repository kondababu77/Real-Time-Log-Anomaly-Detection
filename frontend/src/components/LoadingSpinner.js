import React from 'react';
import { Container, Spinner } from 'react-bootstrap';
import './LoadingSpinner.css';

function LoadingSpinner() {
  return (
    <div className="loading-wrapper">
      <Container>
        <div className="loading-content">
          <Spinner animation="border" variant="primary" role="status" />
          <h4 className="mt-4 text-primary fw-bold">Analyzing your logs...</h4>
          <p className="text-muted">Processing log data and generating comprehensive reports</p>
        </div>
      </Container>
    </div>
  );
}

export default LoadingSpinner;
