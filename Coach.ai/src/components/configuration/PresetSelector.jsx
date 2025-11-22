import React from 'react';

const PresetSelector = ({ config, onSelect }) => {
    if (!config.presets) return null;

    return (
        <div className="card-group" style={{ marginBottom: '2rem' }}>
            {['conservative', 'balanced', 'aggressive'].map(level => (
                <div
                    key={level}
                    className="card"
                    onClick={() => onSelect(level)}
                    style={{
                        cursor: 'pointer',
                        border: '1px solid var(--color-border)',
                        background: 'var(--color-bg-card)',
                        transition: 'transform 0.2s'
                    }}
                >
                    <div className="card-header">
                        <h3>{level.charAt(0).toUpperCase() + level.slice(1)}</h3>
                    </div>
                    <div className="metric-value" style={{ fontSize: '1rem' }}>
                        {config.presets[level].max_seq_length} ctx / {config.presets[level].batch_size} batch
                    </div>
                    <div className="metric-label">
                        {level === 'conservative' ? 'Safe & Stable' : level === 'balanced' ? 'Recommended' : 'Max Performance'}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default PresetSelector;
