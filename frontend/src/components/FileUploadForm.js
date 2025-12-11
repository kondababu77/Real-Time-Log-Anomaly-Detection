import React, { useState } from 'react';
import { Nav, Form, Button } from 'react-bootstrap';
import './FileUploadForm.css';

function FileUploadForm({ onFileUpload, onTextAnalysis }) {
  const [file, setFile] = useState(null);
  const [text, setText] = useState('');
  const [activeTab, setActiveTab] = useState('file');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileSubmit = (e) => {
    e.preventDefault();
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
      onFileUpload(formData);
      setFile(null);
      document.getElementById('file-input').value = '';
    }
  };

  const handleTextSubmit = (e) => {
    e.preventDefault();
    if (text.trim()) {
      onTextAnalysis(text);
      setText('');
    }
  };

  return (
    <div className="upload-form-wrapper">
      <div className="form-header">
        <Nav variant="tabs" activeKey={activeTab} onSelect={(k) => setActiveTab(k)}>
          <Nav.Item>
            <Nav.Link eventKey="file" className="fw-bold">
              <i className="bi bi-file-earmark-arrow-up"></i> Upload File
            </Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link eventKey="text" className="fw-bold">
              <i className="bi bi-pencil-square"></i> Paste Text
            </Nav.Link>
          </Nav.Item>
        </Nav>
      </div>

      <div className="form-content p-4">
        {activeTab === 'file' && (
          <Form onSubmit={handleFileSubmit}>
            <Form.Group className="mb-3">
              <Form.Label className="fw-bold">Select Log File</Form.Label>
              <div className="file-upload-area">
                <Form.Control
                  type="file"
                  id="file-input"
                  accept=".log,.txt"
                  onChange={handleFileChange}
                  className="file-input"
                  required
                />
                <div className="file-upload-content">
                  <div className="file-upload-icon">📁</div>
                  <p className="file-name-display">
                    {file ? file.name : 'Click to select or drag and drop'}
                  </p>
                  <small className="text-muted">Supported formats: .log, .txt (Max 50MB)</small>
                </div>
              </div>
            </Form.Group>
            <Button 
              variant="primary" 
              type="submit" 
              size="lg"
              className="w-100 fw-bold"
              disabled={!file}
            >
              Analyze File
            </Button>
          </Form>
        )}

        {activeTab === 'text' && (
          <Form onSubmit={handleTextSubmit}>
            <Form.Group className="mb-3">
              <Form.Label className="fw-bold">Paste Log Content</Form.Label>
              <Form.Control
                as="textarea"
                id="text-input"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste your log content here. Include multiple lines of log data for comprehensive analysis..."
                rows={8}
                required
                className="form-control-large"
              />
              <Form.Text className="d-block mt-2">
                Paste your log content for immediate analysis
              </Form.Text>
            </Form.Group>
            <Button 
              variant="primary" 
              type="submit" 
              size="lg"
              className="w-100 fw-bold"
              disabled={!text.trim()}
            >
              Analyze Text
            </Button>
          </Form>
        )}
      </div>
    </div>
  );
}

export default FileUploadForm;
