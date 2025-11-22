import React, { useState } from 'react';
import './Steps.css';
import PresetSelector from './configuration/PresetSelector';
import DatasetValidator from './configuration/DatasetValidator';
import HyperparametersForm from './configuration/HyperparametersForm';

const Configuration = ({ config, setConfig, onNext, onPrev }) => {
    const [mode, setMode] = useState('presets'); // 'presets' or 'custom'

    const applyPreset = (presetName) => {
        if (!config.presets) return;
        const p = config.presets[presetName];
        setConfig(prev => ({
            ...prev,
            batchSize: p.batch_size,
            epochs: p.num_epochs,
            gradientAccumulation: p.gradient_accumulation,
            maxSeqLength: p.max_seq_length,
            learningRate: p.learning_rate
        }));
    };

    return (
        <div className="step-container">
            <h2 className="step-title">Training Configuration</h2>
            <p className="step-description">Choose a training strategy or customize parameters.</p>

            {/* Mode Toggle */}
            <div className="mode-toggle" style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
                <button
                    className={`btn ${mode === 'presets' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setMode('presets')}
                >
                    📋 Smart Presets
                </button>
                <button
                    className={`btn ${mode === 'custom' ? 'btn-primary' : 'btn-secondary'}`}
                    onClick={() => setMode('custom')}
                >
                    🎛️ Custom
                </button>
            </div>

            {/* Presets View */}
            {mode === 'presets' && (
                <PresetSelector config={config} onSelect={applyPreset} />
            )}

            {/* Dataset & Model Selection (Always Visible) */}
            <DatasetValidator config={config} setConfig={setConfig} />

            {/* Custom / Advanced Settings */}
            {(mode === 'custom' || !config.presets) && (
                <HyperparametersForm config={config} setConfig={setConfig} />
            )}

            <div className="actions">
                <button className="btn btn-secondary" onClick={onPrev}>Back</button>
                <button className="btn btn-primary" onClick={async () => {
                    try {
                        // Send config to backend
                        const response = await fetch('http://localhost:8000/start-training', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(config)
                        });

                        if (response.ok) {
                            onNext();
                        } else {
                            alert("Failed to start training. Is the backend running?");
                        }
                    } catch (e) {
                        alert("Backend connection failed. Please run 'uvicorn backend.main:app --reload'");
                    }
                }}>Start Training (Real)</button>
            </div>
        </div>
    );
};

export default Configuration;
