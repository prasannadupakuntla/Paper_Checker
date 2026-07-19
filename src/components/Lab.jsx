import { useState, useRef } from 'react';
import { Upload, BrainCircuit, FileText, CheckCircle2, AlertCircle, ArrowLeft, Sparkles, RefreshCw, ShieldCheck, X } from 'lucide-react';
import './lab.css';

const BACKEND_URL = 'http://localhost:8000';

export function Lab({ onBack }) {
    const fileInputRef = useRef(null);
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [imageId, setImageId] = useState('');
    const [evaluating, setEvaluating] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');
    const [activeTab, setActiveTab] = useState('all');

    // Handwriting Calibration State
    const [studentId, setStudentId] = useState('');
    const [isCalibrated, setIsCalibrated] = useState(false);
    const [showCalibrateModal, setShowCalibrateModal] = useState(false);
    const [calibrating, setCalibrating] = useState(false);
    const [calibrationFile, setCalibrationFile] = useState(null);
    const [calibrationImageId, setCalibrationImageId] = useState('');
    const [calibrationResult, setCalibrationResult] = useState(null);
    const [calibrationError, setCalibrationError] = useState('');
    const [referenceText, setReferenceText] = useState(
        "The quick brown fox jumps over the lazy dog. " +
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ " +
        "abcdefghijklmnopqrstuvwxyz " +
        "0123456789 " +
        "Current Voltage Resistance Electricity Circuit Battery Electron Potential Difference"
    );

    const handleFileChange = async (e) => {
        const selectedFile = e.target.files?.[0];
        if (!selectedFile) return;

        setFile(selectedFile);
        setUploading(true);
        setError('');
        setResult(null);
        setImageId('');

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch(`${BACKEND_URL}/upload`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || 'Failed to upload image');
            }

            const data = await response.json();
            setImageId(data.image_id);
        } catch (err) {
            setError(err.message || 'An error occurred during upload.');
            setFile(null);
        } finally {
            setUploading(false);
        }
    };

    const handleCalibrateFileChange = async (e) => {
        const selectedFile = e.target.files?.[0];
        if (!selectedFile) return;

        setCalibrationFile(selectedFile);
        setCalibrating(true);
        setCalibrationError('');
        setCalibrationResult(null);

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch(`${BACKEND_URL}/upload`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || 'Failed to upload image');
            }

            const data = await response.json();
            setCalibrationImageId(data.image_id);
        } catch (err) {
            setCalibrationError(err.message || 'An error occurred during upload.');
            setCalibrationFile(null);
        } finally {
            setCalibrating(false);
        }
    };

    const handleRunCalibration = async () => {
        if (!calibrationImageId || !studentId) return;

        setCalibrating(true);
        setCalibrationError('');

        try {
            const response = await fetch(`${BACKEND_URL}/calibrate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    student_id: studentId,
                    image_id: calibrationImageId,
                    reference_text: referenceText || null
                }),
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || 'Calibration failed');
            }

            const data = await response.json();
            setCalibrationResult(data.profile);
            setIsCalibrated(true);
        } catch (err) {
            setCalibrationError(err.message || 'An error occurred during calibration.');
        } finally {
            setCalibrating(false);
        }
    };

    const handleEvaluate = async () => {
        if (!imageId) return;

        setEvaluating(true);
        setError('');

        try {
            const response = await fetch(`${BACKEND_URL}/evaluate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    image_id: imageId,
                    student_id: studentId || null
                }),
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || 'Evaluation failed');
            }

            const data = await response.json();
            setResult(data);
        } catch (err) {
            setError(err.message || 'An error occurred during evaluation.');
        } finally {
            setEvaluating(false);
        }
    };

    const resetLab = () => {
        setFile(null);
        setImageId('');
        setResult(null);
        setError('');
        // Retain studentId and calibration status for subsequent uploads
    };

    return (
        <div className="lab-container">
            <header className="lab-header">
                <button className="back-btn" onClick={onBack}>
                    <ArrowLeft size={16} /> Back to Landing
                </button>
                <div className="lab-title-wrap">
                    <span className="lab-badge"><Sparkles size={12} /> DEVELOPER LAB</span>
                    <h1>Paper Checker <i>Lab</i></h1>
                    <p>Inspect the internal pipeline stages from image preprocessing to final evaluation.</p>
                </div>
            </header>

            <main className="lab-workspace">
                {error && (
                    <div className="lab-error">
                        <AlertCircle size={18} />
                        <span>{error}</span>
                    </div>
                )}

                {!file && (
                    <div className="lab-upload-zone" onClick={() => fileInputRef.current?.click()}>
                        <div className="upload-icon-wrap">
                            <Upload size={32} />
                        </div>
                        <h3>Upload Student Answer Sheet</h3>
                        <p>Drag and drop or click to browse</p>
                        <span className="file-specs">Supports PNG, JPG, JPEG, PDF up to 10MB</span>
                        <input
                            ref={fileInputRef}
                            type="file"
                            accept="image/*,application/pdf"
                            onChange={handleFileChange}
                            style={{ display: 'none' }}
                        />
                    </div>
                )}

                {file && (
                    <div className="lab-active-session">
                        <div className="session-sidebar">
                            <div className="file-card">
                                <div className="file-info">
                                    <FileText size={24} />
                                    <div>
                                        <h4>{file.name}</h4>
                                        <p>{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                                    </div>
                                </div>
                                {uploading && <div className="status-badge uploading"><RefreshCw size={14} className="spin" /> Uploading...</div>}
                                {imageId && <div className="status-badge ready"><CheckCircle2 size={14} /> Ready for Evaluation</div>}
                            </div>

                            {imageId && (
                                <div className="calibration-section">
                                    <h3>Handwriting Calibration</h3>
                                    <div className="student-id-field">
                                        <label>Student ID</label>
                                        <input
                                            type="text"
                                            placeholder="Optional (e.g. stud_01)"
                                            value={studentId}
                                            onChange={(e) => {
                                                setStudentId(e.target.value);
                                                setIsCalibrated(false);
                                                setCalibrationResult(null);
                                            }}
                                        />
                                    </div>
                                    {studentId && (
                                        <div className="calibration-actions">
                                            {isCalibrated ? (
                                                <div className="calibration-status success">
                                                    <ShieldCheck size={14} /> Calibrated Profile Loaded
                                                </div>
                                            ) : (
                                                <div className="calibration-status pending">
                                                    No profile loaded
                                                </div>
                                            )}
                                            <button
                                                className="calibrate-toggle-btn"
                                                onClick={() => {
                                                    setShowCalibrateModal(true);
                                                    setCalibrationFile(null);
                                                    setCalibrationImageId('');
                                                    setCalibrationResult(null);
                                                    setCalibrationError('');
                                                }}
                                            >
                                                <Sparkles size={14} /> Calibrate Handwriting
                                            </button>
                                        </div>
                                    )}
                                </div>
                            )}

                            {imageId && !result && (
                                <button className="evaluate-btn" onClick={handleEvaluate} disabled={evaluating}>
                                    {evaluating ? (
                                        <>
                                            <RefreshCw size={16} className="spin" /> Running Pipeline...
                                        </>
                                    ) : (
                                        <>
                                            <BrainCircuit size={16} /> Run Evaluation Pipeline
                                        </>
                                    )}
                                </button>
                            )}

                            {result && (
                                <button className="reset-btn" onClick={resetLab}>
                                    Upload Another Paper
                                </button>
                            )}

                            {/* Pipeline Steps Visualization */}
                            <div className="pipeline-steps">
                                <h3>Pipeline Execution</h3>
                                <div className={`step-item ${file ? 'active' : ''}`}>
                                    <span className="step-num">1</span>
                                    <div className="step-details">
                                        <strong>Image Upload</strong>
                                        <p>{imageId ? 'Completed' : uploading ? 'Uploading...' : 'Pending'}</p>
                                    </div>
                                </div>
                                <div className={`step-item ${imageId ? 'active' : ''}`}>
                                    <span className="step-num">2</span>
                                    <div className="step-details">
                                        <strong>Image Preprocessing</strong>
                                        <p>{imageId ? 'Completed (OpenCV)' : 'Pending'}</p>
                                    </div>
                                </div>
                                <div className={`step-item ${evaluating || result ? 'active' : ''}`}>
                                    <span className="step-num">3</span>
                                    <div className="step-details">
                                        <strong>OCR Text Extraction</strong>
                                        <p>{result ? 'Completed (PaddleOCR)' : evaluating ? 'Extracting...' : 'Pending'}</p>
                                    </div>
                                </div>
                                <div className={`step-item ${result ? 'active' : ''}`}>
                                    <span className="step-num">4</span>
                                    <div className="step-details">
                                        <strong>Calibration & Evaluation</strong>
                                        <p>{result ? 'Completed' : evaluating ? 'Evaluating...' : 'Pending'}</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="session-content">
                            {!result && !evaluating && !uploading && (
                                <div className="empty-content-state">
                                    <BrainCircuit size={48} />
                                    <h3>Ready to Evaluate</h3>
                                    <p>Click "Run Evaluation Pipeline" to process the image and view the detailed breakdown.</p>
                                </div>
                            )}

                            {(uploading || evaluating) && (
                                <div className="loading-content-state">
                                    <div className="spinner-orb">
                                        <BrainCircuit size={36} />
                                    </div>
                                    <h3>{uploading ? 'Uploading File...' : 'Processing Pipeline...'}</h3>
                                    <p>{uploading ? 'Saving file to backend storage.' : 'Running image preprocessing, OCR extraction, and evaluation.'}</p>
                                </div>
                            )}

                            {result && (
                                <div className="result-display">
                                    <div className="result-tabs">
                                        {['all', 'image', 'ocr', 'evaluation'].map((tab) => (
                                            <button
                                                key={tab}
                                                className={`tab-btn ${activeTab === tab ? 'active' : ''}`}
                                                onClick={() => setActiveTab(tab)}
                                            >
                                                {tab.toUpperCase()}
                                            </button>
                                        ))}
                                    </div>

                                    <div className="tab-content">
                                        {(activeTab === 'all' || activeTab === 'image') && (
                                            <section className="result-section">
                                                <h3>Original Image</h3>
                                                <div className="image-preview-container">
                                                    <img src={`${BACKEND_URL}${result.original_image_url}`} alt="Uploaded student paper" />
                                                </div>
                                            </section>
                                        )}

                                        {(activeTab === 'all' || activeTab === 'ocr') && (
                                            <div className="ocr-grid">
                                                <section className="result-section">
                                                    <h3>Raw OCR Text</h3>
                                                    <pre className="text-block">{result.ocr_text}</pre>
                                                </section>
                                                <section className="result-section">
                                                    <h3>Corrected OCR (Calibration)</h3>
                                                    <pre className="text-block corrected">{result.corrected_ocr}</pre>
                                                </section>
                                            </div>
                                        )}

                                        {(activeTab === 'all' || activeTab === 'evaluation') && (
                                            <div className="evaluation-grid">
                                                <div className="eval-left">
                                                    <section className="result-section">
                                                        <h3>Retrieved Concept</h3>
                                                        <div className="concept-tag">{result.retrieved_concept}</div>
                                                    </section>
                                                    <section className="result-section">
                                                        <h3>Rubric Used</h3>
                                                        <pre className="text-block rubric">{result.rubric}</pre>
                                                    </section>
                                                </div>
                                                <div className="eval-right">
                                                    <section className="result-section score-section">
                                                        <h3>Confidence & Score</h3>
                                                        <div className="score-card-wrap">
                                                            <div className="score-card">
                                                                <span>SCORE</span>
                                                                <strong>{result.evaluation.split('\n')[0].replace('Score: ', '')}</strong>
                                                            </div>
                                                            <div className="score-card confidence">
                                                                <span>CONFIDENCE</span>
                                                                <strong>{result.confidence}%</strong>
                                                                <span className="conf-label">
                                                                    <ShieldCheck size={14} /> High Trust
                                                                </span>
                                                            </div>
                                                        </div>
                                                    </section>
                                                    <section className="result-section">
                                                        <h3>Evaluation Details</h3>
                                                        <pre className="text-block details">{result.evaluation.substring(result.evaluation.indexOf('\n') + 1)}</pre>
                                                    </section>
                                                    <section className="result-section">
                                                        <h3>Actionable Feedback</h3>
                                                        <pre className="text-block feedback">{result.feedback}</pre>
                                                    </section>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </main>

            {showCalibrateModal && (
                <div className="calibration-modal-overlay">
                    <div className="calibration-modal">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <h2 style={{ margin: 0 }}>Calibrate Handwriting</h2>
                            <button 
                                onClick={() => setShowCalibrateModal(false)}
                                style={{ background: 'none', border: 'none', color: '#9ca3af', cursor: 'pointer' }}
                            >
                                <X size={20} />
                            </button>
                        </div>
                        <p className="description">
                            Upload a sample of student <strong>{studentId}</strong>'s handwriting (calibration sheet) to mine character confusion patterns and physical metrics.
                        </p>

                        <div className="calibration-modal-body">
                            {calibrationError && (
                                <div className="lab-error" style={{ margin: 0 }}>
                                    <AlertCircle size={18} />
                                    <span>{calibrationError}</span>
                                </div>
                            )}

                            {!calibrationFile && (
                                <label className="calibration-upload-btn">
                                    <Upload size={24} style={{ color: '#c084fc' }} />
                                    <span>Upload Calibration Sheet</span>
                                    <span style={{ fontSize: '11px', color: '#6b7280' }}>Click to browse image</span>
                                    <input
                                        type="file"
                                        accept="image/*"
                                        onChange={handleCalibrateFileChange}
                                        style={{ display: 'none' }}
                                    />
                                </label>
                            )}

                            {calibrationFile && (
                                <div className="file-card" style={{ marginBottom: 0 }}>
                                    <div className="file-info" style={{ marginBottom: 0 }}>
                                        <FileText size={20} />
                                        <div>
                                            <h4 style={{ fontSize: '13px', margin: 0 }}>{calibrationFile.name}</h4>
                                            <p style={{ fontSize: '11px', margin: 0 }}>{(calibrationFile.size / 1024 / 1024).toFixed(2)} MB</p>
                                        </div>
                                    </div>
                                    {calibrating && !calibrationImageId && (
                                        <div className="status-badge uploading" style={{ marginTop: '8px' }}>
                                            <RefreshCw size={12} className="spin" /> Uploading...
                                        </div>
                                    )}
                                </div>
                            )}

                            <div className="ref-text-field">
                                <label>Calibration Reference Text</label>
                                <textarea
                                    placeholder="Enter reference text student wrote..."
                                    value={referenceText}
                                    onChange={(e) => setReferenceText(e.target.value)}
                                />
                            </div>

                            {calibrationResult && (
                                <div className="metrics-summary-card">
                                    <h4>Calibration Profile Generated!</h4>
                                    <div className="metrics-grid">
                                        <div className="metric-item">Avg Height: <span>{calibrationResult.physical_metrics?.average_height}px</span></div>
                                        <div className="metric-item">Avg Width: <span>{calibrationResult.physical_metrics?.average_width}px</span></div>
                                        <div className="metric-item">Line Spacing: <span>{calibrationResult.physical_metrics?.line_spacing}px</span></div>
                                        <div className="metric-item">Slant: <span>{calibrationResult.physical_metrics?.slant}°</span></div>
                                    </div>
                                    <div style={{ marginTop: '4px' }}>
                                        <span style={{ fontSize: '11px', color: '#9ca3af', fontWeight: '500' }}>Mined Confusions:</span>
                                        <div className="confusions-list">
                                            {Object.entries(calibrationResult.common_confusions || {}).length > 0 ? (
                                                Object.entries(calibrationResult.common_confusions).map(([ocr, exp]) => (
                                                    <span key={ocr} className="confusion-tag">"{ocr}" ➔ "{exp}"</span>
                                                ))
                                            ) : (
                                                <span style={{ fontSize: '12px', color: '#6b7280', fontStyle: 'italic' }}>None detected (perfect OCR match)</span>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>

                        <div className="calibration-modal-footer">
                            <button className="modal-cancel-btn" onClick={() => setShowCalibrateModal(false)}>
                                Close
                            </button>
                            {calibrationImageId && !calibrationResult && (
                                <button 
                                    className="modal-action-btn" 
                                    onClick={handleRunCalibration}
                                    disabled={calibrating}
                                >
                                    {calibrating ? (
                                        <>
                                            <RefreshCw size={14} className="spin" /> Calibrating...
                                        </>
                                    ) : (
                                        <>
                                            <Sparkles size={14} /> Run Calibration
                                        </>
                                    )}
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
