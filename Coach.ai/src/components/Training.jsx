import React, { useState, useEffect, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Terminal, Activity } from 'lucide-react';
import './Steps.css';

const Training = ({ onNext }) => {
    const [logs, setLogs] = useState([]);
    const [data, setData] = useState([]);
    const [progress, setProgress] = useState(0);
    const scrollRef = useRef(null);

    useEffect(() => {
        const pollInterval = setInterval(async () => {
            try {
                const response = await fetch('http://localhost:8000/training-status');
                if (response.ok) {
                    const statusData = await response.json();

                    // Update Chart
                    if (statusData.data && statusData.data.length > 0) {
                        setData(statusData.data);
                    }

                    // Update Logs
                    if (statusData.logs && statusData.logs.length > 0) {
                        setLogs(statusData.logs);
                    }

                    // Update Progress (Simplified)
                    if (statusData.progress) {
                        // Assuming 100 steps for demo purposes if total not returned
                        setProgress(Math.min(100, statusData.progress));
                    }

                    if (statusData.status === 'completed') {
                        clearInterval(pollInterval);
                        setTimeout(onNext, 1500);
                    }
                }
            } catch (e) {
                console.error("Polling failed", e);
            }
        }, 1000); // Poll every second

        return () => clearInterval(pollInterval);
    }, [onNext]);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [logs]);

    return (
        <div className="step-container">
            <h2 className="step-title">Training in Progress...</h2>

            <div style={{ marginBottom: '2rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <span>Progress</span>
                    <span>{progress}%</span>
                </div>
                <div style={{ height: 8, background: 'var(--color-surface)', borderRadius: 4, overflow: 'hidden' }}>
                    <div style={{
                        width: `${progress}%`, height: '100%',
                        background: 'var(--color-primary)', transition: 'width 0.1s linear'
                    }} />
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1.5rem', height: '400px' }}>
                <div className="card" style={{ display: 'flex', flexDirection: 'column' }}>
                    <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1rem' }}>
                        <Activity size={18} style={{ marginRight: '0.5rem', color: 'var(--color-primary)' }} />
                        <h3>Loss Curve</h3>
                    </div>
                    <div style={{ flex: 1 }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={data}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#233554" />
                                <XAxis dataKey="step" stroke="#8892b0" />
                                <YAxis stroke="#8892b0" />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#112240', border: '1px solid #233554' }}
                                    itemStyle={{ color: '#64ffda' }}
                                />
                                <Line
                                    type="monotone"
                                    dataKey="loss"
                                    stroke="#64ffda"
                                    strokeWidth={2}
                                    dot={false}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="card" style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
                    <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1rem' }}>
                        <Terminal size={18} style={{ marginRight: '0.5rem', color: 'var(--color-primary)' }} />
                        <h3>Live Logs</h3>
                    </div>
                    <div
                        ref={scrollRef}
                        style={{
                            flex: 1, overflowY: 'auto', fontFamily: 'monospace',
                            fontSize: '0.85rem', color: 'var(--color-text-dim)'
                        }}
                    >
                        {logs.map((log, i) => (
                            <div key={i} style={{ marginBottom: '0.25rem' }}>{log}</div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Training;
