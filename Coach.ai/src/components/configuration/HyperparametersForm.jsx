import React from 'react';
import { Sliders } from 'lucide-react';

const HyperparametersForm = ({ config, setConfig }) => {
    return (
        <div className="card">
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1rem' }}>
                <Sliders size={20} style={{ marginRight: '0.5rem', color: 'var(--color-primary)' }} />
                <h3>Advanced Hyperparameters</h3>
            </div>

            <div className="form-group">
                <label>Training Framework</label>
                <select
                    value={config.framework}
                    onChange={(e) => setConfig({ ...config, framework: e.target.value })}
                >
                    <option value="MLX">MLX (Apple Silicon Optimized)</option>
                    <option value="PyTorch">PyTorch (Standard)</option>
                </select>
            </div>

            <div className="form-group">
                <label>Max Sequence Length <span className="tooltip" title="Higher values require more VRAM">ℹ️</span></label>
                <select
                    value={config.maxSeqLength}
                    onChange={(e) => setConfig({ ...config, maxSeqLength: parseInt(e.target.value) })}
                >
                    <option value="128">128 (Minimal)</option>
                    <option value="256">256 (Fastest)</option>
                    <option value="512">512 (Standard)</option>
                    <option value="1024">1024 (Long Context)</option>
                    <option value="2048">2048 (High Memory)</option>
                </select>
            </div>

            <div className="form-group">
                <label>Batch Size: {config.batchSize}</label>
                <input
                    type="range"
                    value={config.batchSize}
                    onChange={(e) => setConfig({ ...config, batchSize: parseInt(e.target.value) })}
                    min="1" max="32"
                />
            </div>

            <div className="form-group">
                <label>Gradient Accumulation: {config.gradientAccumulation}</label>
                <input
                    type="range"
                    value={config.gradientAccumulation}
                    onChange={(e) => setConfig({ ...config, gradientAccumulation: parseInt(e.target.value) })}
                    min="1" max="32"
                />
            </div>

            <div className="form-group">
                <label>Learning Rate</label>
                <input
                    type="number"
                    step="0.00001"
                    value={config.learningRate}
                    onChange={(e) => setConfig({ ...config, learningRate: parseFloat(e.target.value) })}
                />
            </div>

            <div className="form-group">
                <label>Epochs: {config.epochs}</label>
                <input
                    type="range"
                    value={config.epochs}
                    onChange={(e) => setConfig({ ...config, epochs: parseInt(e.target.value) })}
                    min="1" max="10"
                />
            </div>

            <div className="form-group">
                <label>Quantization</label>
                <select
                    name="quantization"
                    value={config.quantization}
                    onChange={(e) => setConfig({ ...config, quantization: e.target.value })}
                >
                    <option value="none">None (FP16)</option>
                    <option value="8-bit">8-bit</option>
                    <option value="4-bit">4-bit (QLoRA)</option>
                </select>
            </div>
        </div>
    );
};

export default HyperparametersForm;
