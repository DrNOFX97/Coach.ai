import React, { useState } from 'react';
import { Upload } from 'lucide-react';

const DatasetValidator = ({ config, setConfig }) => {
    const [validation, setValidation] = useState(null);
    const [isValidating, setIsValidating] = useState(false);

    const handleFileUpload = async (e) => {
        if (!e.target.files || !e.target.files[0]) return;

        const file = e.target.files[0];
        setConfig(prev => ({ ...prev, dataset: file.name }));
        setIsValidating(true);
        setValidation(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const res = await fetch('http://localhost:8000/validate-dataset', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            setValidation(data);
        } catch (err) {
            console.error("Validation failed", err);
            setValidation({ valid_format: false, warnings: ["Validation request failed"] });
        } finally {
            setIsValidating(false);
        }
    };

    return (
        <>
            {/* Validation Card */}
            {validation && (
                <div className="card" style={{
                    borderLeft: validation.valid_format ? '4px solid var(--color-success)' : '4px solid var(--color-error)',
                    marginBottom: '2rem'
                }}>
                    <div className="card-header">
                        <h3>Dataset Health</h3>
                        {isValidating && <span className="loading-spinner"></span>}
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', marginBottom: '1rem' }}>
                        <div>
                            <div className="metric-value">{validation.total_examples}</div>
                            <div className="metric-label">Total Examples</div>
                        </div>
                        <div>
                            <div className="metric-value">{validation.estimated_train} / {validation.estimated_val}</div>
                            <div className="metric-label">Train / Val Split (Est.)</div>
                        </div>
                        <div>
                            <div className="metric-value" style={{ color: validation.valid_format ? 'var(--color-success)' : 'var(--color-error)' }}>
                                {validation.valid_format ? 'Valid JSONL' : 'Invalid Format'}
                            </div>
                            <div className="metric-label">Format Status</div>
                        </div>
                    </div>

                    {validation.warnings.length > 0 && (
                        <div style={{ background: 'rgba(255, 100, 100, 0.1)', padding: '1rem', borderRadius: 8 }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                                <h4 style={{ color: 'var(--color-error)', margin: 0 }}>⚠️ Warnings</h4>
                                {validation.warnings.some(w => w.includes('duplicate')) && (
                                    <button
                                        className="btn btn-sm"
                                        style={{
                                            fontSize: '0.8rem', padding: '0.2rem 0.6rem',
                                            background: 'var(--color-error)', color: 'white', border: 'none'
                                        }}
                                        onClick={async () => {
                                            try {
                                                const res = await fetch('http://localhost:8000/clean-dataset', {
                                                    method: 'POST',
                                                    headers: { 'Content-Type': 'application/json' },
                                                    body: JSON.stringify({ filename: config.dataset })
                                                });
                                                const data = await res.json();
                                                if (data.status === 'success') {
                                                    alert(data.message);
                                                    // Re-trigger validation (upload same file again logic simulation or just refresh)
                                                    // Ideally we re-fetch validation, but for now let's just clear warnings visually or ask user to re-upload
                                                    setValidation(null); // Force re-upload for now to see fresh stats
                                                    alert("Please re-select the file to see updated stats.");
                                                }
                                            } catch (e) {
                                                alert("Failed to clean dataset");
                                            }
                                        }}
                                    >
                                        🛠️ Fix Duplicates
                                    </button>
                                )}
                            </div>
                            <ul style={{ margin: 0, paddingLeft: '1.2rem', fontSize: '0.9rem' }}>
                                {validation.warnings.map((w, i) => <li key={i}>{w}</li>)}
                            </ul>
                        </div>
                    )}
                </div>
            )}

            {/* Upload Input */}
            <div className="card">
                <div className="form-group">
                    <label>Base Model</label>
                    <select
                        name="model"
                        className="input-control"
                        value={config.model}
                        onChange={(e) => setConfig(prev => ({ ...prev, model: e.target.value }))}
                    >
                        <option value="Mistral-7B-v0.1">Mistral 7B (v0.1)</option>
                        <option value="Llama-2-7b">Llama 2 7B</option>
                        <option value="Gemma-7b">Gemma 7B</option>
                    </select>
                </div>

                <div className="input-group">
                    <label>Training Dataset (JSONL)</label>
                    <div
                        style={{
                            border: '2px dashed var(--color-text-dim)',
                            borderRadius: 8, padding: '2rem', textAlign: 'center',
                            cursor: 'pointer', transition: 'border-color 0.2s',
                            position: 'relative'
                        }}
                        onClick={() => document.getElementById('file-upload').click()}
                    >
                        <input
                            id="file-upload"
                            type="file"
                            accept=".jsonl,.csv,.json"
                            style={{ display: 'none' }}
                            onChange={handleFileUpload}
                        />
                        <Upload size={32} style={{ color: 'var(--color-primary)', marginBottom: '1rem' }} />
                        <p>{config.dataset ? config.dataset : 'Drag & drop your dataset here or click to browse'}</p>
                        <p style={{ fontSize: '0.8rem', color: 'var(--color-text-dim)' }}>Supported formats: .jsonl, .csv</p>
                    </div>
                </div>
            </div>
        </>
    );
};

export default DatasetValidator;
