import { useState, useRef } from 'react';
import { Upload, BrainCircuit, FileText, CheckCircle2, AlertCircle, ArrowLeft, Sparkles, RefreshCw, ShieldCheck } from 'lucide-react';
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
                body: JSON.stringify({ image_id: imageId }),
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
        </div>
    );
}
