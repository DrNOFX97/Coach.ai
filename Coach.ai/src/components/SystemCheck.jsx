import React, { useState, useEffect } from 'react';
import { HardDrive, Cpu, Check, AlertCircle } from 'lucide-react';
import './Steps.css';

const SystemCheck = ({ onNext }) => {
    const [checks, setChecks] = useState({
        memory: { status: 'pending', progress: 0, detail: 'Scanning...' },
        disk: { status: 'pending', progress: 0, detail: 'Scanning...' },
        gpu: { status: 'pending', progress: 0, detail: 'Scanning...' }
    });

    const [systemInfo, setSystemInfo] = useState({
        framework: 'Detecting...',
        accelerator: 'Detecting...',
        device_name: 'Scanning...'
    });

    useEffect(() => {
        // Fetch System Info from Backend
        fetch('http://localhost:8000/system-info')
            .then(res => res.json())
            .then(data => setSystemInfo(data))
            .catch(err => console.error("Failed to fetch system info", err));

        const performChecks = async () => {
            // 1. Memory (Approximation)
            const ram = navigator.deviceMemory ? `~${navigator.deviceMemory}GB Available` : '8GB+ (Estimated)';

            // 2. Disk (Async)
            let disk = 'Unknown (Check Permissions)';
            try {
                if (navigator.storage && navigator.storage.estimate) {
                    const estimate = await navigator.storage.estimate();
                    if (estimate.quota) {
                        // Quota is roughly the available space for the origin
                        const availableGB = (estimate.quota / (1024 * 1024 * 1024)).toFixed(0);
                        disk = `~${availableGB}GB Available`;
                    }
                }
            } catch (e) {
                console.error("Storage estimate failed", e);
            }

            // 3. GPU (WebGL Renderer)
            let gpu = 'Integrated Graphics';
            try {
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                if (gl) {
                    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                    if (debugInfo) {
                        gpu = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
                    }
                }
            } catch (e) {
                console.error("WebGL not supported", e);
            }

            // Clean up GPU string
            if (gpu.includes('Apple') && gpu.includes('M')) {
                const match = gpu.match(/Apple M[0-9]+( Pro| Max| Ultra)?/);
                if (match) {
                    gpu = match[0] + " (Metal)";
                }
            } else if (gpu.length > 30) {
                gpu = gpu.substring(0, 30) + '...';
            }

            // Run Animations with Real Data
            const runCheck = (key, resultDetail, duration) => {
                let start = 0;
                const interval = setInterval(() => {
                    start += 5;
                    setChecks(prev => ({
                        ...prev,
                        [key]: { ...prev[key], progress: Math.min(start, 100) }
                    }));
                    if (start >= 100) {
                        clearInterval(interval);
                        setChecks(prev => ({
                            ...prev,
                            [key]: { status: 'success', progress: 100, detail: resultDetail }
                        }));
                    }
                }, duration / 20);
            };

            runCheck('memory', ram, 1500);
            setTimeout(() => runCheck('disk', disk, 1500), 500);
            setTimeout(() => runCheck('gpu', gpu, 2000), 1000);
        };

        performChecks();
    }, []);

    const allPassed = Object.values(checks).every(c => c.status === 'success');

    return (
        <div className="step-container">
            <h2 className="step-title">System Compatibility Check</h2>
            <p className="step-description">Scanning your environment for LLM fine-tuning requirements...</p>

            <div className="card">
                <CheckItem
                    icon={<Cpu />}
                    label="System Memory (RAM)"
                    detail={checks.memory.detail}
                    state={checks.memory}
                />
                <CheckItem
                    icon={<HardDrive />}
                    label="Disk Storage"
                    detail={checks.disk.detail}
                    state={checks.disk}
                />
                <CheckItem
                    icon={<Cpu />}
                    label="GPU Acceleration"
                    detail={checks.gpu.detail}
                    state={checks.gpu}
                />
            </div>

            <div className="card-group"> {/* Using a new div to group these cards */}
                <div className="card">
                    <div className="card-header">
                        <Cpu className="icon" />
                        <h3>Framework</h3>
                    </div>
                    <div className="metric-value">{systemInfo.framework || 'Detecting...'}</div>
                    <div className="metric-label">Optimized for Hardware</div>
                </div>

                <div className="card">
                    <div className="card-header">
                        <Cpu className="icon" />
                        <h3>GPU / Accelerator</h3>
                    </div>
                    <div className="metric-value">{systemInfo.accelerator || 'Detecting...'}</div>
                    <div className="metric-label">{systemInfo.device_name || 'Unknown Device'}</div>
                </div>
            </div>

            <div className="actions">
                <button className="btn btn-primary" onClick={() => onNext({
                    ...systemInfo, // Pass backend info including recommendations
                    ram: checks.memory.detail,
                    gpu: checks.gpu.detail
                })} disabled={!allPassed}>
                    {allPassed ? 'Proceed to Configuration' : 'Scanning...'}
                </button>
            </div>
        </div>
    );
};

const CheckItem = ({ icon, label, detail, state }) => (
    <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div style={{
            width: 40, height: 40, borderRadius: '50%',
            background: 'rgba(100, 255, 218, 0.1)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            color: 'var(--color-primary)', marginRight: '1rem'
        }}>
            {state.status === 'success' ? <Check size={20} /> : icon}
        </div>
        <div style={{ flex: 1 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <span style={{ fontWeight: 600 }}>{label}</span>
                <span style={{ color: 'var(--color-text-dim)' }}>{detail}</span>
            </div>
            <div style={{
                height: 6, background: 'var(--color-bg)', borderRadius: 3, overflow: 'hidden'
            }}>
                <div style={{
                    height: '100%', width: `${state.progress}%`,
                    background: 'var(--color-primary)', transition: 'width 0.2s'
                }} />
            </div>
        </div>
    </div>
);

export default SystemCheck;
