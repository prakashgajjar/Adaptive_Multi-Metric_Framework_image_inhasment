import React, { useState, useRef } from 'react';
import './index.css';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [useAdaptive, setUseAdaptive] = useState(false);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      handleFileSelection(droppedFile);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelection(e.target.files[0]);
    }
  };

  const handleFileSelection = (selectedFile) => {
    if (!selectedFile.type.startsWith('image/')) {
      setError('Please select an image file.');
      return;
    }
    setError(null);
    setFile(selectedFile);
    setPreviewUrl(URL.createObjectURL(selectedFile));
    setResults(null); // Clear previous results
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', file);
    formData.append('adaptive', useAdaptive);

    try {
      const response = await fetch('http://localhost:5000/api/enhance', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error || 'Failed to process image');
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = (base64Data, filename) => {
    const link = document.createElement('a');
    link.href = base64Data;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="container">
      <header className="app-header">
        <h1 className="app-title">Adaptive Image Enhancement</h1>
        <p className="app-subtitle">Upload an image to automatically enhance its quality using multiple algorithms.</p>
      </header>

      {!results && (
        <div className="uploader-card">
          <div 
            className="drop-zone"
            onDragOver={handleDragOver}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current.click()}
          >
            {previewUrl ? (
              <img src={previewUrl} alt="Preview" style={{ maxWidth: '100%', maxHeight: '200px', objectFit: 'contain' }} />
            ) : (
              <>
                <svg className="drop-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
                <p>Drag and drop your image here, or <strong>click to browse</strong></p>
              </>
            )}
            <input 
              type="file" 
              ref={fileInputRef} 
              style={{ display: 'none' }} 
              accept="image/*"
              onChange={handleFileChange}
            />
          </div>

          <label className="checkbox-container">
            <input 
              type="checkbox" 
              checked={useAdaptive} 
              onChange={(e) => setUseAdaptive(e.target.checked)}
            />
            Use adaptive weights for evaluation
          </label>

          {error && <p style={{ color: 'red', marginTop: '1rem' }}>{error}</p>}

          <button 
            className="upload-button" 
            onClick={handleUpload}
            disabled={!file || loading}
          >
            {loading ? <span className="loading-spinner"></span> : 'Enhance Image'}
          </button>
        </div>
      )}

      {results && (
        <div className="results-container">
          <div className="comparison-section">
            <div className="image-card">
              <div className="image-header">
                <span className="image-title">Original</span>
                <button 
                  className="download-btn" 
                  onClick={() => handleDownload(results.original_image, 'original_image.png')}
                  title="Download Original"
                >
                  <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                </button>
              </div>
              <div className="image-wrapper">
                <img src={results.original_image} alt="Original" />
              </div>
            </div>

            <div className="image-card" style={{ borderColor: 'var(--color-black)' }}>
              <div className="image-header">
                <div>
                  <span className="image-title" style={{marginRight: '10px'}}>Best Enhancement</span>
                  <span className="badge">{results.best_method.replace(/_/g, ' ')}</span>
                </div>
                <button 
                  className="download-btn primary" 
                  onClick={() => handleDownload(results.best_image, `best_${results.best_method}.png`)}
                  title="Download Best Result"
                >
                  <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                </button>
              </div>
              <div className="image-wrapper">
                <img src={results.best_image} alt="Best Enhancement" />
              </div>
            </div>
          </div>

          <div className="metrics-section">
            <h3 className="metrics-title">Evaluation Metrics</h3>
            <div className="methods-grid">
              {Object.entries(results.metrics).map(([method, metrics]) => {
                const score = results.composite_scores[method];
                const isBest = method === results.best_method;
                
                return (
                  <div key={method} className={`method-card ${isBest ? 'best' : ''}`}>
                    <div className="method-header">
                      <span className="method-name">{method.replace(/_/g, ' ')}</span>
                      <span className="method-score">Score: {score ? score.toFixed(4) : '0.0000'}</span>
                    </div>
                    <div className="metrics-grid">
                      {Object.entries(metrics).map(([metricName, value]) => (
                        <div key={metricName} className="metric-item">
                          <span className="metric-label">{metricName}</span>
                          <span className="metric-value">{value ? value.toFixed(4) : '0.0000'}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="gallery-section">
            <h3 className="metrics-title">All Enhancements</h3>
            <div className="gallery-grid">
              {Object.entries(results.enhanced_images).map(([method, b64img]) => (
                <div key={method} className="gallery-item">
                  <img src={b64img} alt={method} className="gallery-image" />
                  <div className="gallery-footer">
                    <div className="gallery-label">{method.replace(/_/g, ' ')}</div>
                    <button 
                      className="download-btn small" 
                      onClick={() => handleDownload(b64img, `${method}.png`)}
                      title={`Download ${method}`}
                    >
                      <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          <div style={{ textAlign: 'center', marginTop: '2rem' }}>
            <button 
              className="upload-button" 
              onClick={() => {
                setResults(null);
                setFile(null);
                setPreviewUrl(null);
              }}
            >
              Upload Another Image
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
