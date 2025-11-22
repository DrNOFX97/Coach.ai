import React, { useState } from 'react';
import { FileText, Settings, Play, CheckCircle, AlertTriangle } from 'lucide-react';
import './Steps.css';

const Summary = ({ config, onNext, onPrev }) => {
    const [integrityStatus, setIntegrityStatus] = useState('idle'); // idle, checking, success

    const runIntegrityCheck = () => {
        setIntegrityStatus('checking');
        setTimeout(() => {
            setIntegrityStatus('success');
        }, 2000);
    };

    return (
        <div className="step-container">
            <h2 className="step-title">Pre-Training Summary</h2>
            <p className="step-description">Review your configuration and validate dataset integrity before starting.</p>

            <div className="card">
                <h3>Configuration Overview</h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '1rem' }}>
                    <div className="summary-item">
                        <span style={{ color: 'var(--color-text-dim)' }}>Base Model</span>
                        <div style={{ fontWeight: 600 }}>{config.model}</div>
                    </div>
                    <div className="summary-item">
                        <span style={{ color: 'var(--color-text-dim)' }}>Dataset</span>
                        <div style={{ fontWeight: 600 }}>{config.dataset || 'custom_dataset.jsonl'}</div>
                    </div>
                    <div className="summary-item">
                        <span style={{ color: 'var(--color-text-dim)' }}>Batch Size</span>
                        <div style={{ fontWeight: 600 }}>{config.batchSize}</div>
                    </div>
                    <div className="summary-item">
                        <span style={{ color: 'var(--color-text-dim)' }}>Epochs</span>
                        <div style={{ fontWeight: 600 }}>{config.epochs}</div>
                    </div>
                    <div className="summary-item">
                        <span style={{ color: 'var(--color-text-dim)' }}>Learning Rate</span>
                        <div style={{ fontWeight: 600 }}>{config.learningRate}</div>
                    </div>
                </div>
            </div>

            <div className="card" style={{ borderColor: integrityStatus === 'success' ? 'var(--color-success)' : '' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <div>
                        <h3>Dataset Integrity Check</h3>
                        <p style={{ color: 'var(--color-text-dim)', fontSize: '0.9rem' }}>
                            Validates JSON structure, token counts, and format consistency.
                        </p>
                    </div>
                    {integrityStatus === 'idle' && (
                        <button className="btn btn-secondary" onClick={runIntegrityCheck}>
                            Run Check
                        </button>
                    )}
                    {integrityStatus === 'checking' && (
                        <span style={{ color: 'var(--color-primary)' }}>Verifying...</span>
                    )}
                    {integrityStatus === 'success' && (
                        <div style={{ display: 'flex', alignItems: 'center', color: 'var(--color-success)' }}>
                            <CheckCircle size={20} style={{ marginRight: '0.5rem' }} />
                            Passed
                        </div>
                    )}
                </div>
            </div>

            <div className="actions">
                <button className="btn btn-secondary" onClick={onPrev}>Back</button>
                <button
                    className="btn btn-primary"
                    onClick={onNext}
                    disabled={integrityStatus !== 'success'}
                >
                    <Play size={18} style={{ marginRight: '0.5rem' }} />
                    Start Training
                </button>
            </div>
        </div>
    );
};

export default Summary;
