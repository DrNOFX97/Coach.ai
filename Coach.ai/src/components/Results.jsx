import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { CheckCircle, Download, RefreshCw } from 'lucide-react';
import './Steps.css';

const Results = ({ onRestart }) => {
    const metrics = [
        { name: 'Precision', value: 0.92 },
        { name: 'Recall', value: 0.88 },
        { name: 'F1 Score', value: 0.90 },
        { name: 'Accuracy', value: 0.94 },
    ];

    const radarData = [
        { subject: 'Reasoning', A: 120, fullMark: 150 },
        { subject: 'Coding', A: 98, fullMark: 150 },
        { subject: 'Creativity', A: 86, fullMark: 150 },
        { subject: 'Math', A: 99, fullMark: 150 },
        { subject: 'Language', A: 85, fullMark: 150 },
        { subject: 'Context', A: 65, fullMark: 150 },
    ];

    return (
        <div className="step-container">
            <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
                <div style={{
                    display: 'inline-flex', padding: '1rem', borderRadius: '50%',
                    background: 'rgba(76, 175, 80, 0.1)', color: 'var(--color-success)',
                    marginBottom: '1rem'
                }}>
                    <CheckCircle size={48} />
                </div>
                <h2 className="step-title">Training Completed Successfully!</h2>
                <p className="step-description">Your model has been fine-tuned and is ready for deployment.</p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
                {metrics.map(m => (
                    <div key={m.name} className="card" style={{ textAlign: 'center' }}>
                        <div style={{ fontSize: '0.9rem', color: 'var(--color-text-dim)', marginBottom: '0.5rem' }}>{m.name}</div>
                        <div style={{ fontSize: '2.5rem', fontWeight: 700, color: 'var(--color-primary)' }}>
                            {(m.value * 100).toFixed(1)}%
                        </div>
                    </div>
                ))}
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', height: '350px' }}>
                <div className="card">
                    <h3>Performance Radar</h3>
                    <ResponsiveContainer width="100%" height="100%">
                        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                            <PolarGrid stroke="#233554" />
                            <PolarAngleAxis dataKey="subject" tick={{ fill: '#8892b0' }} />
                            <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} />
                            <Radar name="Model" dataKey="A" stroke="#64ffda" fill="#64ffda" fillOpacity={0.3} />
                        </RadarChart>
                    </ResponsiveContainer>
                </div>

                <div className="card">
                    <h3>Benchmark Comparison</h3>
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={metrics}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#233554" />
                            <XAxis dataKey="name" stroke="#8892b0" />
                            <YAxis stroke="#8892b0" />
                            <Tooltip
                                cursor={{ fill: '#112240' }}
                                contentStyle={{ backgroundColor: '#0a192f', border: '1px solid #233554' }}
                            />
                            <Bar dataKey="value" fill="#64ffda" radius={[4, 4, 0, 0]} />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>

            <div className="actions" style={{ justifyContent: 'center' }}>
                <button className="btn btn-secondary" onClick={onRestart}>
                    <RefreshCw size={18} style={{ marginRight: '0.5rem' }} />
                    Train Another
                </button>
                <button className="btn btn-primary">
                    <Download size={18} style={{ marginRight: '0.5rem' }} />
                    Download Model Weights
                </button>
            </div>
        </div>
    );
};

export default Results;
